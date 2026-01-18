import os
from google import genai

# You will need to set this env var: set/export GEMINI_API_KEY=...
# Or pass it in directly for now if testing

class GeminiRetentionService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY not found. AI features will be disabled.")
            self.client = None
            return
            
        try:
            self.client = genai.Client(api_key=self.api_key)
            print("Gemini client initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            self.client = None

    def generate_retention_content(self, risk_segment: str, context: str) -> dict:
        """
        Generates retention email content using Gemini AI.
        Returns dict with subject_line, email_body, strategy
        """
        if not self.client:
            # Fallback when Gemini is not available - Professional marketing emails
            fallback_emails = {
                "HIGH": {
                    "subject_line": "🎁 Wait! Here's 30% OFF Just For You - Don't Miss Out!",
                    "email_body": """Dear Valued Customer,

We've noticed it's been a while since your last visit, and honestly? We miss you!

As one of our special customers, we want to offer you an EXCLUSIVE deal:

🔥 **30% OFF Your Entire Order** 🔥
Use code: COMEBACK30

But hurry - this offer expires in 48 hours!

Here's what's waiting for you:
✨ New arrivals handpicked based on your preferences
✨ Free shipping on orders over $50
✨ Priority customer support

We value your loyalty and would love to have you back. This is our way of saying "thank you" for being part of our community.

👉 [Shop Now and Save 30%]

Questions? Reply to this email - we're here to help!

Warm regards,
The GrowthAI Team

P.S. This exclusive offer is only available to select customers like you. Don't let it slip away!""",
                    "strategy": "Urgency-driven retention with significant discount (30%) and scarcity tactics for high-risk churning customers"
                },
                "MEDIUM": {
                    "subject_line": "✨ Something Special is Waiting For You Inside...",
                    "email_body": """Hey there!

We've been thinking about you! 💭

While you were away, we've been busy adding some amazing new products and content that we think you'll absolutely LOVE.

Here's what's new:
🆕 Fresh arrivals in your favorite categories
🎯 Personalized picks based on your taste
⭐ Exclusive early access to upcoming releases

And because you're awesome, here's a little something:

💫 **15% OFF Your Next Purchase** 💫
Use code: EXPLORE15

What are you waiting for? Come see what's new!

👉 [Explore New Arrivals]

We can't wait to show you what we've got!

Cheers,
The GrowthAI Team

P.S. Your personalized recommendations are ready and waiting. Trust us, you don't want to miss these!""",
                    "strategy": "Curiosity-driven engagement with moderate incentive (15%) and personalization emphasis for medium-risk customers"
                },
                "LOW": {
                    "subject_line": "💫 Your VIP Picks Are Ready! Plus a Special Thank You Gift",
                    "email_body": """Hello!

Just wanted to drop by and say THANK YOU for being such an amazing customer! 🙏

Because you've been with us, we wanted to share some exclusive picks we think you'll love:

🎯 **Curated Just For You:**
Based on your unique taste, our AI has handpicked items we know you'll enjoy. These aren't random suggestions - they're personalized matches made just for you!

As a token of our appreciation:

🎁 **Enjoy 10% OFF** on your next order
Use code: THANKYOU10

Plus, here's what else you get as a valued member:
✅ Early access to sales
✅ Free shipping on all orders
✅ Exclusive member-only deals

👉 [See Your Personalized Picks]

Thanks for being part of our community. We truly appreciate you!

Best wishes,
The GrowthAI Team

P.S. Keep an eye on your inbox - we've got some exciting surprises coming your way soon! 🎉""",
                    "strategy": "Appreciation-focused retention with loyalty recognition and light incentive (10%) to maintain engagement with low-risk customers"
                }
            }
            return fallback_emails.get(risk_segment, fallback_emails["MEDIUM"])

        # Use Gemini for AI-generated content
        prompt = f"""
        You are an expert retention marketing copywriter.
        
        Task: Write a personalized retention email for a customer.
        
        Risk Level: {risk_segment}
        Context: {context}
        
        Guidelines:
        - HIGH risk: Offer significant discount (25-30%), urgent but not desperate tone
        - MEDIUM risk: Highlight new features/products, moderate incentive (10-15% off)
        - LOW risk: Focus on personalized recommendations, loyalty appreciation
        
        Return ONLY a valid JSON object (no markdown, no code blocks) with these exact keys:
        {{
            "subject_line": "email subject here",
            "email_body": "full email body here with proper formatting",
            "strategy": "brief explanation of the retention strategy used"
        }}
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            clean_text = response.text.strip()
            # Remove markdown code blocks if present
            if clean_text.startswith('```'):
                clean_text = clean_text.split('```')[1]
                if clean_text.startswith('json'):
                    clean_text = clean_text[4:]
            clean_text = clean_text.strip()
            
            import json
            result = json.loads(clean_text)
            return {
                "subject_line": result.get("subject_line", "Special Offer"),
                "email_body": result.get("email_body", "Check out our latest offers!"),
                "strategy": result.get("strategy", "AI-generated retention strategy")
            }
        except Exception as e:
            print(f"Gemini Error: {e}")
            # Return professional fallback templates
            fallback_emails = {
                "HIGH": {
                    "subject_line": "🎁 Wait! Here's 30% OFF Just For You - Don't Miss Out!",
                    "email_body": """Dear Valued Customer,

We've noticed it's been a while since your last visit, and honestly? We miss you!

As one of our special customers, we want to offer you an EXCLUSIVE deal:

🔥 **30% OFF Your Entire Order** 🔥
Use code: COMEBACK30

But hurry - this offer expires in 48 hours!

Here's what's waiting for you:
✨ New arrivals handpicked based on your preferences
✨ Free shipping on orders over $50
✨ Priority customer support

We value your loyalty and would love to have you back.

👉 [Shop Now and Save 30%]

Warm regards,
The GrowthAI Team

P.S. This exclusive offer is only available to select customers like you!""",
                    "strategy": "Urgency-driven retention with significant discount (30%) and scarcity tactics"
                },
                "MEDIUM": {
                    "subject_line": "✨ Something Special is Waiting For You Inside...",
                    "email_body": """Hey there!

We've been thinking about you! 💭

While you were away, we've added amazing new products we think you'll LOVE.

💫 **15% OFF Your Next Purchase** 💫
Use code: EXPLORE15

👉 [Explore New Arrivals]

Cheers,
The GrowthAI Team""",
                    "strategy": "Curiosity-driven engagement with moderate incentive (15%)"
                },
                "LOW": {
                    "subject_line": "💫 Your VIP Picks Are Ready!",
                    "email_body": """Hello!

Thank you for being an amazing customer! 🙏

🎁 **Enjoy 10% OFF** on your next order
Use code: THANKYOU10

👉 [See Your Personalized Picks]

Best wishes,
The GrowthAI Team""",
                    "strategy": "Appreciation-focused retention with loyalty recognition"
                }
            }
            return fallback_emails.get(risk_segment, fallback_emails["MEDIUM"])
