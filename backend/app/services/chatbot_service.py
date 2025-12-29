"""
AI Chatbot Service for Agricultural Assistance
Provides intelligent responses to farming questions
"""

from typing import List, Dict, Optional
import random
from datetime import datetime


class AgriculturalChatbot:
    """AI Chatbot specialized in agricultural advice"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.conversation_history = {}
    
    def _initialize_knowledge_base(self) -> Dict:
        """Initialize agricultural knowledge base"""
        return {
            "watering": {
                "keywords": ["ري", "ماء", "سقي", "watering", "water", "irrigation"],
                "responses": [
                    "💧 نصائح الري: اسقِ النباتات في الصباح الباكر أو المساء لتقليل التبخر. تأكد من أن التربة رطبة وليست مشبعة.",
                    "💧 Watering Tips: Water plants in early morning or evening to reduce evaporation. Ensure soil is moist but not saturated.",
                    "💧 الري الذكي: استخدم نظام الري بالتنقيط لتوفير المياه. راقب رطوبة التربة باستمرار.",
                    "💧 Smart Irrigation: Use drip irrigation systems to save water. Monitor soil moisture regularly."
                ]
            },
            "fertilizer": {
                "keywords": ["سماد", "أسمدة", "fertilizer", "nutrients", "npk"],
                "responses": [
                    "🌱 الأسمدة: استخدم الأسمدة العضوية عند الإمكان. النيتروجين للنمو، الفوسفور للجذور، البوتاسيوم للثمار.",
                    "🌱 Fertilizers: Use organic fertilizers when possible. Nitrogen for growth, Phosphorus for roots, Potassium for fruits.",
                    "🌱 توقيت التسميد: أفضل وقت للتسميد هو بداية موسم النمو. تجنب التسميد في الشتاء.",
                    "🌱 Fertilizing Timing: Best time is at the start of growing season. Avoid fertilizing in winter."
                ]
            },
            "diseases": {
                "keywords": ["مرض", "أمراض", "disease", "sick", "infected"],
                "responses": [
                    "🦠 الأمراض: راقب الأوراق للبقع أو التغيرات في اللون. عزل النباتات المصابة فوراً.",
                    "🦠 Diseases: Monitor leaves for spots or color changes. Isolate infected plants immediately.",
                    "🦠 الوقاية: حافظ على التهوية الجيدة وتجنب الإفراط في الري لمنع الأمراض الفطرية.",
                    "🦠 Prevention: Maintain good ventilation and avoid overwatering to prevent fungal diseases."
                ]
            },
            "pests": {
                "keywords": ["آفات", "حشرات", "pest", "insect", "bug"],
                "responses": [
                    "🐛 الآفات: استخدم المبيدات الطبيعية مثل زيت النيم. شجع الحشرات المفيدة مثل الدعسوقة.",
                    "🐛 Pests: Use natural pesticides like neem oil. Encourage beneficial insects like ladybugs.",
                    "🐛 المكافحة: افحص النباتات بانتظام. يمكنك استخدام صابون مبيد للحشرات كحل طبيعي.",
                    "🐛 Control: Inspect plants regularly. You can use insecticidal soap as a natural solution."
                ]
            },
            "soil": {
                "keywords": ["تربة", "soil", "ground", "earth"],
                "responses": [
                    "🌍 التربة: التربة الجيدة تحتوي على مزيج من الطين والرمل والمواد العضوية. اختبار pH بين 6-7 مثالي.",
                    "🌍 Soil: Good soil contains a mix of clay, sand, and organic matter. pH test between 6-7 is ideal.",
                    "🌍 تحسين التربة: أضف السماد العضوي والسماد الطبيعي لتحسين جودة التربة.",
                    "🌍 Improving Soil: Add compost and organic matter to improve soil quality."
                ]
            },
            "general": {
                "keywords": ["مساعدة", "نصيحة", "help", "advice", "suggestion"],
                "responses": [
                    "🌱 أنا مساعدك الذكي في الزراعة! يمكنني مساعدتك في الري، الأسمدة، الأمراض، الآفات، والتربة. اسألني أي شيء!",
                    "🌱 I'm your smart farming assistant! I can help with watering, fertilizers, diseases, pests, and soil. Ask me anything!",
                    "🌱 نصيحة عامة: راقب نباتاتك يومياً. التغييرات الصغيرة يمكن أن تشير إلى مشاكل كبيرة.",
                    "🌱 General Tip: Monitor your plants daily. Small changes can indicate big problems."
                ]
            }
        }
    
    def get_response(self, user_id: int, message: str, language: str = "ar") -> Dict:
        """
        Get chatbot response based on user message
        
        Args:
            user_id: User ID for conversation history
            message: User's message
            language: Language preference (ar/en)
        
        Returns:
            Dict with response and metadata
        """
        message_lower = message.lower()
        
        # Check conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Find matching topic
        matched_topic = None
        max_matches = 0
        
        for topic, data in self.knowledge_base.items():
            matches = sum(1 for keyword in data["keywords"] if keyword in message_lower)
            if matches > max_matches:
                max_matches = matches
                matched_topic = topic
        
        # Get response
        if matched_topic and max_matches > 0:
            responses = self.knowledge_base[matched_topic]["responses"]
            # Filter by language preference
            if language == "ar":
                filtered_responses = [r for r in responses if any(c in r for c in "💧🌱🦠🐛🌍")]
            else:
                filtered_responses = [r for r in responses if not any(c in r for c in "💧🌱🦠🐛🌍") or "Watering" in r or "Fertilizers" in r]
            
            if not filtered_responses:
                filtered_responses = responses
            
            response_text = random.choice(filtered_responses)
        else:
            # Default response
            if language == "ar":
                response_text = "🌱 لم أفهم سؤالك تماماً. يمكنك أن تسألني عن الري، الأسمدة، الأمراض، الآفات، أو التربة. كيف يمكنني مساعدتك؟"
            else:
                response_text = "🌱 I didn't fully understand your question. You can ask me about watering, fertilizers, diseases, pests, or soil. How can I help?"
        
        # Save to history
        self.conversation_history[user_id].append({
            "user_message": message,
            "bot_response": response_text,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep only last 20 messages
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
        
        return {
            "response": response_text,
            "topic": matched_topic or "general",
            "confidence": min(max_matches / 3, 1.0) if max_matches > 0 else 0.3,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_conversation_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get conversation history for user"""
        if user_id not in self.conversation_history:
            return []
        return self.conversation_history[user_id][-limit:]
    
    def clear_history(self, user_id: int):
        """Clear conversation history for user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Global chatbot instance
chatbot = AgriculturalChatbot()


