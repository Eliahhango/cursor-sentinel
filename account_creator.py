"""
Cursor-Sentinel: Automated Account Creator
One-click account creation using Playwright with temporary email
"""

import asyncio
import json
import random
import string
import time
from pathlib import Path
from typing import Optional, Dict, Tuple

try:
    from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class AccountCreator:
    """Automated account creator using Playwright"""
    
    def __init__(self):
        self.playwright_available = PLAYWRIGHT_AVAILABLE
        self.temp_email_services = [
            "https://tempmail.io/",
            "https://10minutemail.com/",
            "https://guerrillamail.com/",
        ]
        self.cursor_signup_url = "https://cursor.sh/auth/signup"
    
    def generate_random_email(self, domain: str = "tempmail.io") -> str:
        """Generate random email address"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return f"{username}@{domain}"
    
    def generate_random_password(self, length: int = 16) -> str:
        """Generate random secure password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))
    
    async def get_temp_email(self, page: Page, service_url: str) -> Optional[str]:
        """Get temporary email from service"""
        try:
            await page.goto(service_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Try to extract email from common temp mail services
            # This is a generic approach - may need service-specific selectors
            email_selectors = [
                'input[readonly]',
                'input[type="email"]',
                '#email',
                '.email',
                '[id*="email"]',
                '[class*="email"]'
            ]
            
            for selector in email_selectors:
                try:
                    email_element = await page.query_selector(selector)
                    if email_element:
                        email = await email_element.get_attribute('value') or await email_element.input_value()
                        if email and '@' in email:
                            return email
                except Exception:
                    continue
            
            # Fallback: generate random email
            return self.generate_random_email()
        
        except Exception as e:
            print(f"Error getting temp email: {e}")
            return self.generate_random_email()
    
    async def wait_for_verification_email(self, page: Page, timeout: int = 120) -> Optional[str]:
        """Wait for verification email and extract verification link"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Refresh email inbox
                await page.reload(wait_until="networkidle")
                await asyncio.sleep(3)
                
                # Look for email link/code
                link_selectors = [
                    'a[href*="verif"]',
                    'a[href*="confirm"]',
                    'a[href*="verify"]',
                    'a[href*="cursor"]',
                    '.email-body a',
                    '[class*="link"]'
                ]
                
                for selector in link_selectors:
                    try:
                        link_element = await page.query_selector(selector)
                        if link_element:
                            href = await link_element.get_attribute('href')
                            if href and ('cursor' in href.lower() or 'verif' in href.lower()):
                                return href
                    except Exception:
                        continue
                
            except Exception:
                pass
            
            await asyncio.sleep(5)
        
        return None
    
    async def create_cursor_account(self, email: Optional[str] = None, password: Optional[str] = None) -> Tuple[bool, Dict[str, str]]:
        """Create Cursor account using Playwright automation"""
        if not self.playwright_available:
            return False, {"error": "Playwright not installed. Install with: pip install playwright && playwright install"}
        
        if not email:
            email = self.generate_random_email()
        if not password:
            password = self.generate_random_password()
        
        result = {
            "email": email,
            "password": password,
            "status": "pending"
        }
        
        try:
            async with async_playwright() as p:
                # Launch browser (headless=False for debugging, set to True for production)
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                
                # Step 1: Get temporary email
                temp_email_page = await context.new_page()
                temp_email = await self.get_temp_email(temp_email_page, self.temp_email_services[0])
                temp_email_page.close()
                
                if not temp_email:
                    result["error"] = "Failed to get temporary email"
                    await browser.close()
                    return False, result
                
                result["temp_email"] = temp_email
                email = temp_email  # Use temp email
                result["email"] = email
                
                # Step 2: Navigate to Cursor signup
                signup_page = await context.new_page()
                await signup_page.goto(self.cursor_signup_url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)
                
                # Step 3: Fill signup form
                try:
                    # Find email input
                    email_input = await signup_page.wait_for_selector(
                        'input[type="email"], input[name*="email"], #email',
                        timeout=10000
                    )
                    await email_input.fill(email)
                    await asyncio.sleep(1)
                    
                    # Find password input
                    password_input = await signup_page.wait_for_selector(
                        'input[type="password"], input[name*="password"], #password',
                        timeout=10000
                    )
                    await password_input.fill(password)
                    await asyncio.sleep(1)
                    
                    # Find and click submit button
                    submit_button = await signup_page.wait_for_selector(
                        'button[type="submit"], button:has-text("Sign up"), button:has-text("Create"), .signup-button',
                        timeout=10000
                    )
                    await submit_button.click()
                    await asyncio.sleep(3)
                    
                    # Step 4: Wait for verification email
                    inbox_page = await context.new_page()
                    await inbox_page.goto(self.temp_email_services[0], wait_until="networkidle")
                    await asyncio.sleep(2)
                    
                    verification_link = await self.wait_for_verification_email(inbox_page, timeout=120)
                    inbox_page.close()
                    
                    if verification_link:
                        # Step 5: Click verification link
                        await signup_page.goto(verification_link, wait_until="networkidle")
                        await asyncio.sleep(3)
                        result["status"] = "verified"
                        result["verification_link"] = verification_link
                    else:
                        result["status"] = "pending_verification"
                        result["warning"] = "Could not auto-verify. Check email manually."
                    
                    signup_page.close()
                    await browser.close()
                    
                    result["success"] = True
                    return True, result
                
                except PlaywrightTimeout as e:
                    result["error"] = f"Timeout during signup: {str(e)}"
                    await browser.close()
                    return False, result
                except Exception as e:
                    result["error"] = f"Signup failed: {str(e)}"
                    await browser.close()
                    return False, result
        
        except Exception as e:
            result["error"] = f"Account creation failed: {str(e)}"
            return False, result
    
    def create_account_sync(self, email: Optional[str] = None, password: Optional[str] = None) -> Tuple[bool, Dict[str, str]]:
        """Synchronous wrapper for create_cursor_account"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.create_cursor_account(email, password))
    
    def save_account_credentials(self, credentials: Dict[str, str], profile_name: str) -> bool:
        """Save account credentials to profile"""
        try:
            profiles_dir = Path.home() / ".cursor-sentinel" / "profiles"
            profiles_dir.mkdir(parents=True, exist_ok=True)
            
            profile_file = profiles_dir / f"{profile_name}_credentials.json"
            
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(credentials, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
