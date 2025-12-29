"""
Enhanced AI Chatbot Service
Advanced chatbot with comprehensive agricultural knowledge
"""

from typing import List, Dict, Optional
import random
from datetime import datetime
from sqlalchemy.orm import Session
from app import models


class EnhancedAgriculturalChatbot:
    """Enhanced AI Chatbot with comprehensive knowledge"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_comprehensive_knowledge_base()
        self.conversation_history = {}
    
    def _initialize_comprehensive_knowledge_base(self) -> Dict:
        """Initialize comprehensive agricultural knowledge base"""
        return {
            "watering": {
                "keywords": ["ري", "ماء", "سقي", "رطوبة", "watering", "water", "irrigation", "moisture", "hydrate"],
                "responses_ar": [
                    "💧 **نصائح الري الذكية:**\n• اسقِ النباتات في الصباح الباكر (6-8 صباحاً) أو المساء (6-8 مساءً)\n• تجنب الري في منتصف النهار لتقليل التبخر\n• تأكد من أن التربة رطبة وليست مشبعة بالماء\n• استخدم نظام الري بالتنقيط لتوفير المياه\n• راقب رطوبة التربة يومياً",
                    "💧 **كمية الري:**\n• النباتات الصغيرة: 0.5-1 لتر يومياً\n• النباتات المتوسطة: 2-3 لتر يومياً\n• النباتات الكبيرة: 5-8 لتر يومياً\n• في الصيف: زد الكمية بنسبة 30%\n• في الشتاء: قلل الكمية بنسبة 50%",
                    "💧 **علامات نقص الماء:**\n• ذبول الأوراق\n• جفاف التربة\n• اصفرار الأوراق\n• توقف النمو\n• سقوط الأوراق"
                ],
                "responses_en": [
                    "💧 **Smart Watering Tips:**\n• Water plants in early morning (6-8 AM) or evening (6-8 PM)\n• Avoid watering at midday to reduce evaporation\n• Ensure soil is moist but not waterlogged\n• Use drip irrigation systems to save water\n• Monitor soil moisture daily",
                    "💧 **Watering Amount:**\n• Small plants: 0.5-1 liter daily\n• Medium plants: 2-3 liters daily\n• Large plants: 5-8 liters daily\n• In summer: Increase by 30%\n• In winter: Reduce by 50%",
                    "💧 **Signs of Water Deficiency:**\n• Wilting leaves\n• Dry soil\n• Yellowing leaves\n• Stunted growth\n• Leaf drop"
                ]
            },
            "fertilizer": {
                "keywords": ["سماد", "أسمدة", "تسميد", "npk", "نيتروجين", "فوسفور", "بوتاسيوم", "fertilizer", "nutrients", "npk", "nitrogen", "phosphorus", "potassium"],
                "responses_ar": [
                    "🌱 **الأسمدة الأساسية (NPK):**\n• **النيتروجين (N):** للنمو الخضري والأوراق - استخدم في الربيع والصيف\n• **الفوسفور (P):** للجذور والزهور - استخدم عند الزراعة\n• **البوتاسيوم (K):** للثمار والمقاومة - استخدم قبل الإثمار\n• **النسبة المثالية:** 10-10-10 أو 20-20-20",
                    "🌱 **أنواع الأسمدة:**\n• **عضوية:** سماد طبيعي، سماد دودي، سماد حيواني - آمنة وطويلة الأمد\n• **كيميائية:** سريعة المفعول لكن قد تضر بالتربة\n• **سائلة:** سهلة الاستخدام، امتصاص سريع\n• **حبيبية:** بطيئة الإطلاق، تدوم طويلاً",
                    "🌱 **متى تسمد:**\n• **الربيع:** بداية موسم النمو - كل أسبوعين\n• **الصيف:** ذروة النمو - كل أسبوع\n• **الخريف:** تقليل التسميد - كل شهر\n• **الشتاء:** توقف التسميد (معظم النباتات)"
                ],
                "responses_en": [
                    "🌱 **Essential Fertilizers (NPK):**\n• **Nitrogen (N):** For vegetative growth and leaves - use in spring and summer\n• **Phosphorus (P):** For roots and flowers - use at planting\n• **Potassium (K):** For fruits and resistance - use before fruiting\n• **Ideal Ratio:** 10-10-10 or 20-20-20",
                    "🌱 **Fertilizer Types:**\n• **Organic:** Natural compost, worm castings, manure - safe and long-lasting\n• **Chemical:** Fast-acting but may harm soil\n• **Liquid:** Easy to use, fast absorption\n• **Granular:** Slow-release, long-lasting",
                    "🌱 **When to Fertilize:**\n• **Spring:** Start of growing season - every 2 weeks\n• **Summer:** Peak growth - weekly\n• **Autumn:** Reduce fertilization - monthly\n• **Winter:** Stop fertilizing (most plants)"
                ]
            },
            "diseases": {
                "keywords": ["مرض", "أمراض", "عدوى", "فطريات", "بكتيريا", "disease", "sick", "infected", "fungus", "bacteria", "infection"],
                "responses_ar": [
                    "🦠 **أمراض النباتات الشائعة:**\n• **البياض الدقيقي:** بقع بيضاء على الأوراق - استخدم مبيد فطري\n• **اللفحة:** بقع بنية/سوداء - عزل النبات المصاب\n• **العفن:** رطوبة زائدة - حسّن التهوية\n• **الصدأ:** بقع برتقالية - رش بمبيد فطري\n• **الذبول:** نقص ماء أو عدوى - فحص الجذور",
                    "🦠 **الوقاية من الأمراض:**\n• حافظ على التهوية الجيدة\n• تجنب الإفراط في الري\n• استخدم تربة معقمة\n• نظف الأدوات قبل الاستخدام\n• راقب النباتات يومياً\n• عزل النباتات المصابة فوراً",
                    "🦠 **المعالجة الطبيعية:**\n• **زيت النيم:** مضاد فطري طبيعي\n• **صودا الخبز:** للبياض الدقيقي (1 ملعقة + لتر ماء)\n• **الثوم:** مضاد بكتيري طبيعي\n• **القرفة:** مضاد فطري\n• **خل التفاح:** توازن pH التربة"
                ],
                "responses_en": [
                    "🦠 **Common Plant Diseases:**\n• **Powdery Mildew:** White spots on leaves - use fungicide\n• **Blight:** Brown/black spots - isolate infected plant\n• **Mold:** Excess moisture - improve ventilation\n• **Rust:** Orange spots - spray with fungicide\n• **Wilt:** Water deficiency or infection - check roots",
                    "🦠 **Disease Prevention:**\n• Maintain good ventilation\n• Avoid overwatering\n• Use sterilized soil\n• Clean tools before use\n• Monitor plants daily\n• Isolate infected plants immediately",
                    "🦠 **Natural Treatments:**\n• **Neem Oil:** Natural fungicide\n• **Baking Soda:** For powdery mildew (1 tbsp + 1 liter water)\n• **Garlic:** Natural antibacterial\n• **Cinnamon:** Antifungal\n• **Apple Cider Vinegar:** Balance soil pH"
                ]
            },
            "pests": {
                "keywords": ["آفات", "حشرات", "حشرة", "من", "ذباب", "عثة", "pest", "insect", "bug", "aphid", "fly", "moth"],
                "responses_ar": [
                    "🐛 **الآفات الشائعة:**\n• **المن:** حشرات صغيرة خضراء/سوداء - استخدم صابون مبيد\n• **الذباب الأبيض:** حشرات بيضاء صغيرة - مصائد لاصقة\n• **العث:** شبكات على الأوراق - رش بزيت النيم\n• **الديدان:** ثقوب في الأوراق - جمع يدوي أو مبيد\n• **النمل:** يحمي المن - عالج المن أولاً",
                    "🐛 **المكافحة الطبيعية:**\n• **زيت النيم:** مبيد حشري طبيعي شامل\n• **صابون مبيد:** للآفات الرخوة (2 ملعقة + لتر ماء)\n• **الثوم والفلفل:** رش طارد للحشرات\n• **النباتات الطاردة:** الريحان، النعناع، القطيفة\n• **الحشرات المفيدة:** الدعسوقة، العناكب، الدبابير",
                    "🐛 **الوقاية:**\n• افحص النباتات أسبوعياً\n• نظف الأوراق الميتة\n• استخدم تربة نظيفة\n• تجنب الإفراط في التسميد\n• شجع الحشرات المفيدة بزراعة نباتات جاذبة"
                ],
                "responses_en": [
                    "🐛 **Common Pests:**\n• **Aphids:** Small green/black insects - use insecticidal soap\n• **Whiteflies:** Small white insects - sticky traps\n• **Spider Mites:** Webs on leaves - spray with neem oil\n• **Caterpillars:** Holes in leaves - handpick or pesticide\n• **Ants:** Protect aphids - treat aphids first",
                    "🐛 **Natural Control:**\n• **Neem Oil:** Natural broad-spectrum insecticide\n• **Insecticidal Soap:** For soft-bodied pests (2 tbsp + 1 liter water)\n• **Garlic & Pepper:** Insect-repelling spray\n• **Repellent Plants:** Basil, mint, marigold\n• **Beneficial Insects:** Ladybugs, spiders, wasps",
                    "🐛 **Prevention:**\n• Inspect plants weekly\n• Clean dead leaves\n• Use clean soil\n• Avoid over-fertilization\n• Encourage beneficial insects with attractive plants"
                ]
            },
            "soil": {
                "keywords": ["تربة", "أرض", "تراب", "ph", "حموضة", "قلوية", "soil", "ground", "earth", "ph", "acidity", "alkaline"],
                "responses_ar": [
                    "🌍 **أنواع التربة:**\n• **طينية:** تحتفظ بالماء لكن ثقيلة - أضف رمل ومواد عضوية\n• **رملية:** تصرف جيد لكن تفقد الماء - أضف طين ومواد عضوية\n• **طميية:** مثالية - توازن جيد\n• **عضوية:** غنية بالمغذيات - أفضل للزراعة",
                    "🌍 **pH التربة:**\n• **6.0-7.0:** مثالي لمعظم النباتات\n• **أقل من 6.0:** حمضية - أضف جير\n• **أكثر من 7.0:** قلوية - أضف كبريت\n• **اختبار pH:** استخدم شرائط الاختبار أو مقياس رقمي",
                    "🌍 **تحسين التربة:**\n• أضف السماد العضوي (30% من التربة)\n• استخدم السماد الطبيعي\n• أضف الفيرميكوليت للصرف\n• استخدم المهاد (mulch) للاحتفاظ بالرطوبة\n• اقلب التربة سنوياً"
                ],
                "responses_en": [
                    "🌍 **Soil Types:**\n• **Clay:** Retains water but heavy - add sand and organic matter\n• **Sandy:** Good drainage but loses water - add clay and organic matter\n• **Loamy:** Ideal - good balance\n• **Organic:** Rich in nutrients - best for planting",
                    "🌍 **Soil pH:**\n• **6.0-7.0:** Ideal for most plants\n• **Below 6.0:** Acidic - add lime\n• **Above 7.0:** Alkaline - add sulfur\n• **Test pH:** Use test strips or digital meter",
                    "🌍 **Improving Soil:**\n• Add organic compost (30% of soil)\n• Use natural manure\n• Add vermiculite for drainage\n• Use mulch to retain moisture\n• Turn soil annually"
                ]
            },
            "general": {
                "keywords": ["مساعدة", "نصيحة", "معلومات", "كيف", "ماذا", "help", "advice", "info", "how", "what"],
                "responses_ar": [
                    "🌱 **مرحباً! أنا مساعدك الذكي في الزراعة**\n\nيمكنني مساعدتك في:\n• 💧 الري وإدارة المياه\n• 🌱 الأسمدة والتغذية\n• 🦠 الأمراض والعلاج\n• 🐛 الآفات والمكافحة\n• 🌍 التربة والتحسين\n• 📊 التحليلات والإحصائيات\n\nاسألني أي شيء عن الزراعة!",
                    "🌱 **نصائح عامة للنجاح:**\n• راقب نباتاتك يومياً\n• سجل ملاحظاتك\n• اتبع جدول ري منتظم\n• استخدم أسمدة متوازنة\n• حافظ على التهوية الجيدة\n• عالج المشاكل مبكراً"
                ],
                "responses_en": [
                    "🌱 **Hello! I'm your smart farming assistant**\n\nI can help with:\n• 💧 Watering and water management\n• 🌱 Fertilizers and nutrition\n• 🦠 Diseases and treatment\n• 🐛 Pests and control\n• 🌍 Soil and improvement\n• 📊 Analysis and statistics\n\nAsk me anything about farming!",
                    "🌱 **General Success Tips:**\n• Monitor your plants daily\n• Keep notes\n• Follow regular watering schedule\n• Use balanced fertilizers\n• Maintain good ventilation\n• Treat problems early"
                ]
            }
        }
    
    def get_response(self, user_id: int, message: str, language: str = "ar", db: Session = None) -> Dict:
        """
        Get enhanced chatbot response
        
        Args:
            user_id: User ID
            message: User message
            language: Language (ar/en)
            db: Database session (for user-specific data)
        
        Returns:
            Response dict
        """
        message_lower = message.lower().strip()
        
        # Check conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Get user's recent analyses for context
        user_context = self._get_user_context(user_id, db) if db else None
        
        # Find best matching topic
        matched_topic = None
        max_matches = 0
        
        for topic, data in self.knowledge_base.items():
            matches = sum(1 for keyword in data["keywords"] if keyword in message_lower)
            if matches > max_matches:
                max_matches = matches
                matched_topic = topic
        
        # Generate response
        if matched_topic and max_matches > 0:
            responses = self.knowledge_base[matched_topic][f"responses_{language}"]
            response_text = random.choice(responses)
            
            # Add user-specific context if available
            if user_context and matched_topic in ["watering", "fertilizer", "diseases"]:
                response_text += f"\n\n📊 **حالتك الحالية:**\n{user_context}"
        else:
            # Intelligent fallback - try to understand the question
            response_text = self._generate_intelligent_response(message_lower, language, user_context)
        
        # Save to history
        self.conversation_history[user_id].append({
            "user_message": message,
            "bot_response": response_text,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep last 50 messages
        if len(self.conversation_history[user_id]) > 50:
            self.conversation_history[user_id] = self.conversation_history[user_id][-50:]
        
        return {
            "response": response_text,
            "topic": matched_topic or "general",
            "confidence": min(max_matches / 3, 1.0) if max_matches > 0 else 0.5,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_user_context(self, user_id: int, db: Session) -> Optional[str]:
        """Get user's current plant status for context"""
        try:
            recent_analysis = db.query(models.Analysis).filter(
                models.Analysis.user_id == user_id
            ).order_by(models.Analysis.created_at.desc()).first()
            
            if not recent_analysis:
                return None
            
            context_parts = []
            if recent_analysis.plant_health_score:
                context_parts.append(f"صحة النبات: {recent_analysis.plant_health_score:.0f}%")
            if recent_analysis.water_needs:
                context_parts.append(f"احتياجات المياه: {recent_analysis.water_needs:.1f} لتر/يوم")
            if recent_analysis.diseases:
                context_parts.append(f"الأمراض المكتشفة: {len(recent_analysis.diseases)}")
            
            return " | ".join(context_parts) if context_parts else None
        except:
            return None
    
    def _generate_intelligent_response(self, message: str, language: str, context: Optional[str]) -> str:
        """Generate intelligent response for unrecognized questions"""
        # Check for question words
        question_words_ar = ["كيف", "ماذا", "متى", "أين", "لماذا", "كم"]
        question_words_en = ["how", "what", "when", "where", "why", "how much", "how many"]
        
        is_question = any(word in message for word in question_words_ar + question_words_en)
        
        if language == "ar":
            if is_question:
                return "🌱 سؤال جيد! يمكنني مساعدتك في:\n• 💧 الري والمياه\n• 🌱 الأسمدة والتغذية\n• 🦠 الأمراض والعلاج\n• 🐛 الآفات والمكافحة\n• 🌍 التربة\n\nجرب أن تسأل بشكل أكثر تحديداً، مثلاً: 'كيف أروي نباتاتي؟' أو 'ما أفضل سماد للطماطم؟'"
            else:
                return "🌱 أفهم! يمكنك أن تسألني عن:\n• 💧 الري وإدارة المياه\n• 🌱 الأسمدة والتغذية\n• 🦠 الأمراض والعلاج\n• 🐛 الآفات والمكافحة\n• 🌍 التربة والتحسين\n\nمثال: 'كيف أروي نباتاتي؟' أو 'ما أفضل وقت للتسميد؟'"
        else:
            if is_question:
                return "🌱 Good question! I can help with:\n• 💧 Watering and water management\n• 🌱 Fertilizers and nutrition\n• 🦠 Diseases and treatment\n• 🐛 Pests and control\n• 🌍 Soil\n\nTry asking more specifically, e.g., 'How do I water my plants?' or 'What's the best fertilizer for tomatoes?'"
            else:
                return "🌱 I understand! You can ask me about:\n• 💧 Watering and water management\n• 🌱 Fertilizers and nutrition\n• 🦠 Diseases and treatment\n• 🐛 Pests and control\n• 🌍 Soil and improvement\n\nExample: 'How do I water my plants?' or 'What's the best time to fertilize?'"
    
    def get_conversation_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get conversation history"""
        if user_id not in self.conversation_history:
            return []
        return self.conversation_history[user_id][-limit:]
    
    def clear_history(self, user_id: int):
        """Clear conversation history"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Global enhanced chatbot instance
enhanced_chatbot = EnhancedAgriculturalChatbot()

