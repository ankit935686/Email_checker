from flask import Flask, render_template, request, jsonify
import asyncio
import trio
import httpx
from holehe.core import get_functions, import_submodules
import json
import threading
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to store results
results_cache = {}

def run_holehe_async(email):
    """Run holehe asynchronously and store results"""
    async def main():
        try:
            # Import all modules
            modules = import_submodules("holehe.modules")
            websites = get_functions(modules)
            
            # Initialize client with timeout
            client = httpx.AsyncClient(timeout=30.0)
            out = []
            
            # Process each website sequentially to avoid async issues
            total_websites = len(websites)
            for i, website in enumerate(websites, 1):
                try:
                    await website(email, client, out)
                    # Update progress in cache
                    results_cache[email]['progress'] = f"{i}/{total_websites}"
                    logger.info(f"Processed {i}/{total_websites} websites for {email}")
                except Exception as e:
                    logger.warning(f"Error in module {website.__name__ if hasattr(website, '__name__') else 'unknown'}: {str(e)}")
            
            await client.aclose()
            
            # Process results
            processed_results = []
            for result in out:
                if isinstance(result, dict):
                    processed_results.append({
                        'name': result.get('name', 'Unknown'),
                        'exists': result.get('exists', False),
                        'rateLimit': result.get('rateLimit', False),
                        'emailrecovery': result.get('emailrecovery', ''),
                        'phoneNumber': result.get('phoneNumber', ''),
                        'others': result.get('others', '')
                    })
            
            # Count found accounts for logging
            found_results = [r for r in processed_results if r.get('exists', False)]
            logger.info(f"Found {len(found_results)} accounts with exists=True")
            for result in found_results:
                logger.info(f"Found account: {result.get('name', 'Unknown')} - exists: {result.get('exists')}")
            
            # Store results in cache
            results_cache[email] = {
                'status': 'completed',
                'results': processed_results,
                'timestamp': datetime.now().isoformat(),
                'total_sites': len(processed_results),
                'found_accounts': len(found_results)
            }
            logger.info(f"Analysis completed for {email}: {len(processed_results)} results")
            
        except Exception as e:
            logger.error(f"Error processing email {email}: {str(e)}")
            results_cache[email] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    # Run the async function
    trio.run(main)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if we already have results for this email
    if email in results_cache:
        return jsonify(results_cache[email])
    
    # Mark as processing
    results_cache[email] = {
        'status': 'processing',
        'timestamp': datetime.now().isoformat()
    }
    
    # Start processing in background thread
    thread = threading.Thread(target=run_holehe_async, args=(email,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'processing', 'message': 'Analysis started'})

@app.route('/get_results/<email>')
def get_results(email):
    if email in results_cache:
        result = results_cache[email]
        logger.info(f"Returning results for {email}: {result['status']}")
        return jsonify(result)
    else:
        return jsonify({'error': 'No results found for this email'}), 404

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    results_cache.clear()
    return jsonify({'message': 'Cache cleared successfully'})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 