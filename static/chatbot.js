// KHARY AI Assistant - Professional Version
(function() {
    // Check if chat already exists
    if(document.getElementById('khary-ai-chat')) return;

    // Chat memory - stores conversation history
let conversationHistory = [];

// Maximum messages to remember (prevents too long history)
const MAX_HISTORY = 20;
    
    // Comprehensive knowledge base
    const knowledgeBase = {
        scholarships: {
            china: "🎓 CSC Scholarship (China):\n• Full tuition waiver\n• Free accommodation\n• Monthly stipend: 3,000-3,500 RMB\n• Health insurance\n• Deadline: January-March",
            korea: "🎓 KGSP Scholarship (Korea):\n• Full tuition\n• Monthly stipend: 1,000,000 KRW\n• Airfare reimbursement\n• Korean language training\n• Deadline: February-March",
            japan: "🎓 MEXT Scholarship (Japan):\n• Full tuition\n• Monthly stipend: 117,000-145,000 JPY\n• Airfare\n• Deadline: April-May",
            singapore: "🎓 ASEAN Scholarship (Singapore):\n• Full tuition at NUS/NTU/SMU\n• Living allowance: SGD 5,800/year\n• Deadline: February-March",
            malaysia: "🎓 Malaysia International Scholarship:\n• Tuition fees\n• Monthly allowance: RM 1,500\n• Deadline: April-May"
        },
        universities: {
            china: "🇨🇳 Top Universities in China:\n• Tsinghua University (QS #25)\n• Peking University (QS #17)\n• Fudan University (QS #34)\n• Shanghai Jiao Tong University (QS #46)\n• Zhejiang University (QS #44)\n• University of Science and Technology (QS #93)\n• Nanjing University (QS #133)\n• Wuhan University (QS #194)",
            singapore: "🇸🇬 Top Universities in Singapore:\n• National University of Singapore (QS #8)\n• Nanyang Technological University (QS #26)\n• Singapore Management University\n• Singapore University of Technology and Design",
            malaysia: "🇲🇾 Top Universities in Malaysia:\n• University of Malaya (QS #65)\n• Universiti Putra Malaysia (QS #158)\n• Universiti Kebangsaan Malaysia (QS #129)\n• Universiti Sains Malaysia (QS #146)\n• Universiti Teknologi Malaysia (QS #188)",
            japan: "🇯🇵 Top Universities in Japan:\n• University of Tokyo (QS #23)\n• Kyoto University (QS #46)\n• Osaka University (QS #68)\n• Tohoku University (QS #79)\n• Tokyo Institute of Technology (QS #91)",
            korea: "🇰🇷 Top Universities in Korea:\n• Seoul National University (QS #29)\n• KAIST (QS #42)\n• Yonsei University (QS #73)\n• Korea University (QS #79)\n• POSTECH (QS #81)"
        },
        fees: {
            china: "💰 China Tuition Fees:\n• Bachelor: $3,000-6,000/year\n• Master: $3,500-7,000/year\n• PhD: $4,000-8,000/year",
            singapore: "💰 Singapore Tuition Fees:\n• Bachelor: SGD 22,000-30,000/year\n• Master: SGD 25,000-40,000/year\n• PhD: SGD 20,000-35,000/year",
            malaysia: "💰 Malaysia Tuition Fees:\n• Bachelor: $2,500-5,300/year\n• Master: $3,000-6,000/year\n• PhD: $3,500-7,000/year",
            japan: "💰 Japan Tuition Fees:\n• Bachelor: $3,600-5,000/year\n• Master: $4,000-6,000/year\n• PhD: $4,500-7,000/year",
            korea: "💰 Korea Tuition Fees:\n• Bachelor: $3,800-6,000/year\n• Master: $4,500-7,500/year\n• PhD: $5,000-8,000/year"
        },
        livingCost: {
            china: "🏠 Living Cost China:\n• Accommodation: $200-500/month\n• Food: $150-300/month\n• Transport: $30-50/month\n• Utilities: $50-80/month\n• Total: $500-1,000/month",
            singapore: "🏠 Living Cost Singapore:\n• Accommodation: SGD 400-1,000/month\n• Food: SGD 300-500/month\n• Transport: SGD 80-120/month\n• Utilities: SGD 100-150/month\n• Total: SGD 1,000-2,000/month",
            malaysia: "🏠 Living Cost Malaysia:\n• Accommodation: RM 400-1,000/month\n• Food: RM 300-600/month\n• Transport: RM 50-100/month\n• Utilities: RM 100-150/month\n• Total: RM 1,000-2,000/month",
            japan: "🏠 Living Cost Japan:\n• Accommodation: JPY 40,000-80,000/month\n• Food: JPY 30,000-50,000/month\n• Transport: JPY 10,000-15,000/month\n• Utilities: JPY 10,000-20,000/month\n• Total: JPY 100,000-160,000/month",
            korea: "🏠 Living Cost Korea:\n• Accommodation: KRW 400,000-800,000/month\n• Food: KRW 300,000-500,000/month\n• Transport: KRW 50,000-100,000/month\n• Utilities: KRW 100,000-150,000/month\n• Total: KRW 900,000-1,500,000/month"
        },
        duration: {
            bachelor: "🎓 Bachelor's Duration:\n• China: 4 years\n• Singapore: 3-4 years\n• Malaysia: 3-4 years\n• Japan: 4 years\n• Korea: 4 years",
            master: "📚 Master's Duration:\n• China: 2-3 years\n• Singapore: 1-2 years\n• Malaysia: 1-2 years\n• Japan: 2 years\n• Korea: 2 years",
            phd: "🔬 PhD Duration:\n• China: 3-5 years\n• Singapore: 3-5 years\n• Malaysia: 3-5 years\n• Japan: 3-5 years\n• Korea: 3-5 years",
            language: "🗣️ Language Course Duration:\n• Intensive: 4-12 weeks\n• Semester: 4-6 months\n• Year: 10-12 months\n• HSK/JLPT/TOPIK Prep: 8-12 weeks"
        },
        requirements: {
            bachelor: "📝 Bachelor's Requirements:\n• High School Diploma (70-85%+)\n• IELTS 6.0-6.5 or TOEFL 80-90\n• Personal statement\n• Recommendation letters (2)\n• Passport copy",
            master: "📝 Master's Requirements:\n• Bachelor's degree (GPA 3.0/4.0+)\n• IELTS 6.5-7.0 or TOEFL 90-100\n• GRE/GMAT (for some programs)\n• Work experience (for MBA)\n• Research proposal (for research degrees)",
            phd: "📝 PhD Requirements:\n• Master's degree (GPA 3.5/4.0+)\n• IELTS 7.0+ or TOEFL 100+\n• Research publications (preferred)\n• Detailed research proposal\n• 2-3 academic references"
        },
        deadlines: {
            china: "📅 China Deadlines:\n• Fall (September intake): March-May\n• Spring (February intake): October-November\n• CSC Scholarship: January-March",
            singapore: "📅 Singapore Deadlines:\n• Fall (August intake): February-March\n• Spring (January intake): August-September\n• Scholarship: January-February",
            malaysia: "📅 Malaysia Deadlines:\n• Fall (September intake): May-June\n• Spring (February intake): November-December\n• Scholarship: April-May",
            japan: "📅 Japan Deadlines:\n• Fall (October intake): January-February\n• Spring (April intake): August-September\n• MEXT Scholarship: April-May",
            korea: "📅 Korea Deadlines:\n• Fall (September intake): April-May\n• Spring (March intake): October-November\n• KGSP Scholarship: February-March"
        },
        visa: {
            china: "🇨🇳 China Student Visa (X1/X2):\n• JW202 form from university\n• Admission letter\n• Medical examination\n• Financial proof ($3,000+)\n• Processing: 4-6 weeks\n• Visa fee: $150-200",
            singapore: "🇸🇬 Singapore Student Pass:\n• SOLAR application online\n• Medical report\n• Financial proof (SGD 15,000+)\n• Processing: 2-4 weeks\n• Fee: SGD 90",
            malaysia: "🇲🇾 Malaysia Student Visa:\n• VAL application\n• Medical exam\n• Financial proof (RM 10,000+)\n• Processing: 4-8 weeks\n• Fee: RM 500-1,000",
            japan: "🇯🇵 Japan Student Visa:\n• COE (Certificate of Eligibility)\n• Financial proof (JPY 2,000,000+)\n• Study plan\n• Processing: 1-3 months\n• Fee: JPY 3,000",
            korea: "🇰🇷 Korea Student Visa (D-2):\n• Admission letter\n• Financial proof ($10,000+)\n• Health certificate\n• Processing: 2-4 weeks\n• Fee: KRW 60,000"
        },
        parttime: {
            china: "💼 Part-time Work China:\n• 20 hours/week during term\n• Full-time during holidays\n• Pay: 20-50 RMB/hour\n• Popular jobs: English teacher, cafe, intern",
            singapore: "💼 Part-time Work Singapore:\n• 16 hours/week during term\n• Full-time during holidays\n• Pay: SGD 8-15/hour\n• Popular jobs: F&B, retail, tutor",
            malaysia: "💼 Part-time Work Malaysia:\n• 20 hours/week during breaks\n• Pay: RM 8-15/hour\n• Popular jobs: retail, F&B, event staff",
            japan: "💼 Part-time Work Japan:\n• 28 hours/week with permission\n• Pay: JPY 900-1,200/hour\n• Popular jobs: convenience store, restaurant, tutor",
            korea: "💼 Part-time Work Korea:\n• 20 hours/week after 6 months\n• Pay: KRW 8,720-10,000/hour\n• Popular jobs: cafe, restaurant, admin"
        },
        housing: {
            china: "🏠 Housing China:\n• On-campus dorm: $200-500/month\n• Off-campus apartment: $400-800/month\n• Homestay: $300-600/month\n• Deposit: 1-2 months rent",
            singapore: "🏠 Housing Singapore:\n• University hostel: SGD 400-800/month\n• HDB room rental: SGD 500-1,000/month\n• Private apartment: SGD 800-2,000/month",
            malaysia: "🏠 Housing Malaysia:\n• On-campus: RM 300-800/month\n• Off-campus: RM 500-1,500/month\n• Condo: RM 1,000-2,000/month",
            japan: "🏠 Housing Japan:\n• Dormitory: JPY 30,000-60,000/month\n• Share house: JPY 40,000-80,000/month\n• Apartment: JPY 60,000-120,000/month",
            korea: "🏠 Housing Korea:\n• University dorm: KRW 300,000-600,000/month\n• One-room: KRW 400,000-800,000/month\n• Officetel: KRW 600,000-1,000,000/month"
        },
        documents: [
            "📄 Academic transcripts (all years with translation)",
            "🎓 Degree certificates/High school diploma (notarized)",
            "🌍 Language test scores (IELTS/TOEFL/HSK/JLPT/TOPIK)",
            "📖 Passport copy (valid for 1+ years)",
            "📝 Statement of Purpose (SOP) - 500-1000 words",
            "✉️ Recommendation letters (2-3 academic/professional)",
            "💰 Bank statement (financial proof - 6 months)",
            "🏥 Medical examination report",
            "📸 Passport size photos (4-6 copies)",
            "📋 CV/Resume (for graduate programs)"
        ]
    };

    // Chat Widget HTML
    const chatHTML = `
    <div id="khary-ai-chat" style="position: fixed; bottom: 70px; right: 25px; z-index: 99999; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;">
        <!-- Chat Button -->
        <div id="khary-chat-button" style="width: 60px; height: 60px; background: linear-gradient(135deg, #1E3A8A, #2D4FA8); border-radius: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: all 0.3s ease; position: relative;">
            <i class="fas fa-comment-dots" style="font-size: 28px; color: white;"></i>
            <span style="position: absolute; top: -5px; right: -5px; width: 12px; height: 12px; background: #10B981; border-radius: 50%; border: 2px solid white;"></span>
        </div>
        
        <!-- Chat Window -->
        <div id="khary-chat-window" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; height: 550px; max-height: 70vh; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.15); overflow: hidden; flex-direction: column; z-index: 100001;">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-robot" style="font-size: 22px; color: white;"></i>
                    </div>
                    <div>
                        <div style="font-weight: 600; font-size: 16px; color: white;">KHARY AI Assistant</div>
                        <div style="font-size: 11px; color: rgba(255,255,255,0.8);">Online • 24/7 Support</div>
                    </div>
                    <button id="clear-chat" style="background: none; border: none; color: rgba(255,255,255,0.8); font-size: 16px; cursor: pointer; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">🗑️</button>
                </div>
                <button id="khary-close-chat" style="background: none; border: none; color: rgba(255,255,255,0.8); font-size: 20px; cursor: pointer; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;">✕</button>
            </div>
            
            <!-- Messages Area -->
            <div id="khary-chat-messages" style="flex: 1; overflow-y: auto; padding: 20px; background: #F8FAFC;">
                <div style="display: flex; margin-bottom: 15px;">
                    <div style="max-width: 85%; background: #1E3A8A; color: white; padding: 12px 16px; border-radius: 18px; border-bottom-left-radius: 4px; font-size: 14px; line-height: 1.5;">
                        👋 <strong>Welcome to KHARY Global EDU!</strong><br><br>
                        I'm your study abroad assistant. Ask me anything about:<br><br>
                        📚 Universities & Programs<br>
                        💰 Scholarships & Funding<br>
                        📝 Application Process<br>
                        🌏 Country Information<br>
                        💵 Fees & Living Costs<br>
                        🎫 Visa Guidance<br>
                        🏠 Housing & Part-time Jobs<br>
                        📅 Deadlines & Requirements
                    </div>
                </div>
            </div>
            
            <!-- Quick Questions - Horizontal Scroll at Bottom -->
<div style="padding: 10px 12px; background: white; border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;">
    <div style="font-size: 9px; color: #64748B; margin-bottom: 6px; font-weight: 600;">POPULAR QUESTIONS (Click to ask)</div>
    <div style="display: flex; flex-wrap: nowrap; gap: 8px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px;">

            
                    <button class="khary-quick-q" data-q="scholarships">💰 Scholarships</button>
                    <button class="khary-quick-q" data-q="china">🇨🇳 China</button>
                    <button class="khary-quick-q" data-q="singapore">🇸🇬 Singapore</button>
                    <button class="khary-quick-q" data-q="malaysia">🇲🇾 Malaysia</button>
                    <button class="khary-quick-q" data-q="japan">🇯🇵 Japan</button>
                    <button class="khary-quick-q" data-q="korea">🇰🇷 Korea</button>
                    <button class="khary-quick-q" data-q="fees">💰 Tuition Fees</button>
                    <button class="khary-quick-q" data-q="livingcost">🏠 Living Cost</button>
                    <button class="khary-quick-q" data-q="bachelor">🎓 Bachelor Duration</button>
                    <button class="khary-quick-q" data-q="master">📚 Master Duration</button>
                    <button class="khary-quick-q" data-q="phd">🔬 PhD Duration</button>
                    <button class="khary-quick-q" data-q="requirements">📝 Requirements</button>
                    <button class="khary-quick-q" data-q="documents">📋 Documents</button>
                    <button class="khary-quick-q" data-q="deadlines">📅 Deadlines</button>
                    <button class="khary-quick-q" data-q="visa">🎫 Visa Process</button>
                    <button class="khary-quick-q" data-q="parttime">💼 Part-time Jobs</button>
                    <button class="khary-quick-q" data-q="housing">🏠 Accommodation</button>
                    <button class="khary-quick-q" data-q="csc">🇨🇳 CSC Scholarship</button>
                    <button class="khary-quick-q" data-q="kgsp">🇰🇷 KGSP Scholarship</button>
                    <button class="khary-quick-q" data-q="mext">🇯🇵 MEXT Scholarship</button>
                    <button class="khary-quick-q" data-q="asean">🇸🇬 ASEAN Scholarship</button>
                    <button class="khary-quick-q" data-q="ielts">📖 IELTS Requirement</button>
                    <button class="khary-quick-q" data-q="toefl">📖 TOEFL Requirement</button>
                    <button class="khary-quick-q" data-q="apply">📝 How to Apply</button>
                    <button class="khary-quick-q" data-q="contact">📞 Contact Us</button>
                    <button class="khary-quick-q" data-q="intake">📅 Intake Seasons</button>
                    <button class="khary-quick-q" data-q="hsktest">🇨🇳 HSK Test</button>
                    <button class="khary-quick-q" data-q="jlpt">🇯🇵 JLPT Test</button>
                    <button class="khary-quick-q" data-q="topik">🇰🇷 TOPIK Test</button>
                    <button class="khary-quick-q" data-q="language">🗣️ Language Courses</button>
                    <button class="khary-quick-q" data-q="health">🏥 Health Insurance</button>
                </div>
            </div>
            
            <!-- Input Area -->
            <div style="padding: 15px; background: white; border-top: 1px solid #E2E8F0; display: flex; gap: 12px;">
                <input type="text" id="khary-chat-input" placeholder="Type your question here..." style="flex: 1; padding: 12px 16px; border: 1px solid #E2E8F0; border-radius: 30px; font-size: 14px; outline: none; transition: all 0.2s;">
                <button id="khary-send-chat" style="width: 44px; height: 44px; background: #1E3A8A; border: none; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s;">
                    <i class="fas fa-paper-plane" style="color: white; font-size: 16px;"></i>
                </button>
            </div>
        </div>
    </div>
    
    <style>
        .khary-quick-q {
            background: #EFF6FF;
            border: 1px solid #1E3A8A;
            color: #1E3A8A;
            padding: 5px 12px;
            border-radius: 25px;
            font-size: 11px;
            font-weight: 500;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .khary-quick-q:hover {
            background: #1E3A8A;
            color: white;
            transform: translateY(-1px);
        }
        #khary-chat-messages::-webkit-scrollbar {
            width: 5px;
        }
        #khary-chat-messages::-webkit-scrollbar-track {
            background: #E2E8F0;
            border-radius: 10px;
        }
        #khary-chat-messages::-webkit-scrollbar-thumb {
            background: #1E3A8A;
            border-radius: 10px;
        }
        #khary-chat-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.25);
        }
        #khary-chat-input:focus {
            border-color: #1E3A8A;
            box-shadow: 0 0 0 2px rgba(30,58,138,0.1);
        }
        .khary-quick-q-container {
            scrollbar-width: thin;
        }
        @media (max-width: 500px) {
            #khary-chat-window { width: 340px; right: -10px; height: 550px; }
            .khary-quick-q { padding: 4px 10px; font-size: 10px; }
        }
    </style>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatHTML);
    
    // DOM elements
    const chatButton = document.getElementById('khary-chat-button');
    const chatWindow = document.getElementById('khary-chat-window');
    const closeChat = document.getElementById('khary-close-chat');
    const chatInput = document.getElementById('khary-chat-input');
    const sendButton = document.getElementById('khary-send-chat');
    const chatMessages = document.getElementById('khary-chat-messages');
    
    let isOpen = false;
    
    // Toggle chat
    if(chatButton) {
        chatButton.addEventListener('click', () => {
            if(isOpen) {
                chatWindow.style.display = 'none';
                isOpen = false;
            } else {
                chatWindow.style.display = 'flex';
                isOpen = true;
            }
        });
    }
    
    if(closeChat) {
    closeChat.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        isOpen = false;
    });
}

const clearChat = document.getElementById('clear-chat');
if(clearChat) {
    clearChat.addEventListener('click', () => {
        conversationHistory = [];
        if(chatMessages) {
            chatMessages.innerHTML = '<div style="display: flex; margin-bottom: 15px;"><div style="max-width: 85%; background: #1E3A8A; color: white; padding: 12px 16px; border-radius: 18px; border-bottom-left-radius: 4px; font-size: 14px; line-height: 1.5;">👋 <strong>Welcome to KHARY Global EDU!</strong><br><br>Chat history cleared. Ask me anything!</div></div>';
        }
    });
}
    
    function addMessage(text, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.style.display = 'flex';
    messageDiv.style.marginBottom = '12px';
    messageDiv.style.justifyContent = isUser ? 'flex-end' : 'flex-start';
    
    const bubble = document.createElement('div');
    bubble.style.padding = '10px 14px';
    bubble.style.borderRadius = '18px';
    bubble.style.maxWidth = '80%';
    bubble.style.whiteSpace = 'pre-line';
    bubble.style.fontSize = '14px';
    bubble.style.lineHeight = '1.5';
    
    if(isUser) {
        bubble.style.background = '#D4AF37';
        bubble.style.color = '#1E3A8A';
        bubble.style.borderBottomRightRadius = '4px';
    } else {
        bubble.style.background = '#1E3A8A';
        bubble.style.color = 'white';
        bubble.style.borderBottomLeftRadius = '4px';
    }
    
    bubble.innerHTML = text;
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Store in conversation history
    conversationHistory.push({ role: isUser ? 'user' : 'assistant', content: text });
    
    // Keep only last MAX_HISTORY messages
    if(conversationHistory.length > MAX_HISTORY) {
        conversationHistory = conversationHistory.slice(-MAX_HISTORY);
    }
}
    
    function getAnswer(question) {
    const q = question.toLowerCase();
    
    // Check if question relates to previous conversation
    let context = "";
    if(conversationHistory.length > 0) {
        const lastQuestion = conversationHistory.filter(m => m.role === 'user').pop();
        if(lastQuestion) {
            context = ` (User previously asked about: ${lastQuestion.content.substring(0, 50)})`;
        }
    }
    
    // ===== SCHOLARSHIPS =====
    if(q.includes('scholarship') || q.includes('funding') || q.includes('financial aid')) {
        if(q.includes('china') || q.includes('csc')) return knowledgeBase.scholarships.china;
        if(q.includes('korea') || q.includes('kgsp')) return knowledgeBase.scholarships.korea;
        if(q.includes('japan') || q.includes('mext')) return knowledgeBase.scholarships.japan;
        if(q.includes('singapore') || q.includes('asean')) return knowledgeBase.scholarships.singapore;
        if(q.includes('malaysia')) return knowledgeBase.scholarships.malaysia;
        return "🎓 Available Scholarships:\n\n🇨🇳 CSC (China)\n🇰🇷 KGSP (Korea)\n🇯🇵 MEXT (Japan)\n🇸🇬 ASEAN (Singapore)\n🇲🇾 MIS (Malaysia)\n\nWhich country interests you?";
    }
    
    // ===== UNIVERSITIES =====
    if(q.includes('university') || q.includes('universities') || q.includes('study in')) {
        if(q.includes('china')) return knowledgeBase.universities.china;
        if(q.includes('singapore')) return knowledgeBase.universities.singapore;
        if(q.includes('malaysia')) return knowledgeBase.universities.malaysia;
        if(q.includes('japan')) return knowledgeBase.universities.japan;
        if(q.includes('korea')) return knowledgeBase.universities.korea;
        return "🏛️ Which country are you interested in for university information? (China, Singapore, Malaysia, Japan, Korea)";
    }
    
    // ===== FEES =====
    if(q.includes('fee') || q.includes('tuition') || q.includes('cost') || q.includes('price')) {
        if(q.includes('china')) return knowledgeBase.fees.china;
        if(q.includes('singapore')) return knowledgeBase.fees.singapore;
        if(q.includes('malaysia')) return knowledgeBase.fees.malaysia;
        if(q.includes('japan')) return knowledgeBase.fees.japan;
        if(q.includes('korea')) return knowledgeBase.fees.korea;
        return "💰 Which country's tuition fees would you like to know? (China, Singapore, Malaysia, Japan, Korea)";
    }
    
    // ===== LIVING COST =====
    if(q.includes('living') || q.includes('cost of living') || q.includes('accommodation cost')) {
        if(q.includes('china')) return knowledgeBase.livingCost.china;
        if(q.includes('singapore')) return knowledgeBase.livingCost.singapore;
        if(q.includes('malaysia')) return knowledgeBase.livingCost.malaysia;
        if(q.includes('japan')) return knowledgeBase.livingCost.japan;
        if(q.includes('korea')) return knowledgeBase.livingCost.korea;
        return "🏠 Which country's living cost would you like to know?";
    }
    
    // ===== DURATION =====
    if(q.includes('duration') || q.includes('how long') || q.includes('years')) {
        if(q.includes('bachelor') || q.includes('undergraduate')) return knowledgeBase.duration.bachelor;
        if(q.includes('master')) return knowledgeBase.duration.master;
        if(q.includes('phd') || q.includes('doctorate')) return knowledgeBase.duration.phd;
        if(q.includes('language')) return knowledgeBase.duration.language;
        return "🎓 Which program duration would you like to know? (Bachelor, Master, PhD, Language)";
    }
    
    // ===== REQUIREMENTS =====
    if(q.includes('requirement') || q.includes('eligibility') || q.includes('qualification') || q.includes('need to apply')) {
        if(q.includes('bachelor') || q.includes('undergraduate')) return knowledgeBase.requirements.bachelor;
        if(q.includes('master')) return knowledgeBase.requirements.master;
        if(q.includes('phd') || q.includes('doctorate')) return knowledgeBase.requirements.phd;
        return "📝 Which program requirements would you like to know? (Bachelor, Master, PhD)";
    }
    
    // ===== DOCUMENTS =====
    if(q.includes('document') || q.includes('required paper') || q.includes('what do i need') || q.includes('paperwork')) {
        return "📋 Required Documents for Application:\n\n" + knowledgeBase.documents.join('\n');
    }
    
    // ===== DEADLINES =====
    if(q.includes('deadline') || q.includes('when to apply') || q.includes('intake') || q.includes('application deadline')) {
        if(q.includes('china')) return knowledgeBase.deadlines.china;
        if(q.includes('singapore')) return knowledgeBase.deadlines.singapore;
        if(q.includes('malaysia')) return knowledgeBase.deadlines.malaysia;
        if(q.includes('japan')) return knowledgeBase.deadlines.japan;
        if(q.includes('korea')) return knowledgeBase.deadlines.korea;
        return "📅 Which country's application deadlines would you like to know?";
    }
    
    // ===== VISA =====
    if(q.includes('visa') || q.includes('student visa') || q.includes('immigration')) {
        if(q.includes('china')) return knowledgeBase.visa.china;
        if(q.includes('singapore')) return knowledgeBase.visa.singapore;
        if(q.includes('malaysia')) return knowledgeBase.visa.malaysia;
        if(q.includes('japan')) return knowledgeBase.visa.japan;
        if(q.includes('korea')) return knowledgeBase.visa.korea;
        return "🎫 Which country's student visa information would you like?";
    }
    
    // ===== PART-TIME JOBS =====
    if(q.includes('part time') || q.includes('work') || q.includes('job') || q.includes('employment') || q.includes('working')) {
        if(q.includes('china')) return knowledgeBase.parttime.china;
        if(q.includes('singapore')) return knowledgeBase.parttime.singapore;
        if(q.includes('malaysia')) return knowledgeBase.parttime.malaysia;
        if(q.includes('japan')) return knowledgeBase.parttime.japan;
        if(q.includes('korea')) return knowledgeBase.parttime.korea;
        return "💼 Which country's part-time work information would you like?";
    }
    
    // ===== HOUSING =====
    if(q.includes('housing') || q.includes('accommodation') || q.includes('dorm') || q.includes('stay') || q.includes('rent') || q.includes('apartment')) {
        if(q.includes('china')) return knowledgeBase.housing.china;
        if(q.includes('singapore')) return knowledgeBase.housing.singapore;
        if(q.includes('malaysia')) return knowledgeBase.housing.malaysia;
        if(q.includes('japan')) return knowledgeBase.housing.japan;
        if(q.includes('korea')) return knowledgeBase.housing.korea;
        return "🏠 Which country's housing information would you like?";
    }
    
    // ===== LANGUAGE TESTS =====
    if(q.includes('ielts')) {
        return "📖 IELTS Requirement:\n• Bachelor: 6.0-6.5 overall\n• Master: 6.5-7.0 overall\n• PhD: 7.0+ overall\n• No band less than 5.5-6.0\n• Valid for 2 years";
    }
    if(q.includes('toefl')) {
        return "📖 TOEFL Requirement:\n• Bachelor: 80-90 iBT\n• Master: 90-100 iBT\n• PhD: 100+ iBT\n• Valid for 2 years";
    }
    if(q.includes('hsk')) {
        return "🇨🇳 HSK Test (Chinese):\n• HSK 4: For Bachelor programs\n• HSK 5: For Master programs\n• HSK 6: For PhD programs\n• Test dates: Monthly\n• Results: 1 month";
    }
    if(q.includes('jlpt')) {
        return "🇯🇵 JLPT Test (Japanese):\n• N5-N4: Beginner\n• N3: Intermediate\n• N2-N1: Advanced\n• Test: July & December\n• Results: 2 months";
    }
    if(q.includes('topik')) {
        return "🇰🇷 TOPIK Test (Korean):\n• TOPIK 1: Level 1-2\n• TOPIK 2: Level 3-6\n• Level 3-4: Undergraduate\n• Level 5-6: Graduate\n• Test: Jan, Apr, May, Jul, Oct, Nov";
    }
    
    // ===== HEALTH INSURANCE =====
    if(q.includes('health') || q.includes('insurance') || q.includes('medical')) {
        return "🏥 Health Insurance:\n• All countries require health insurance\n• Cost: $100-500/year\n• Most universities provide group insurance\n• Covers basic medical services";
    }
    
    // ===== LANGUAGE COURSES =====
    if(q.includes('language course') || q.includes('learn') || q.includes('study language')) {
        return "🗣️ Language Courses Available:\n\n🇨🇳 Chinese (HSK 1-6): 4-12 weeks\n🇯🇵 Japanese (JLPT N5-N1): 4-12 weeks\n🇰🇷 Korean (TOPIK 1-6): 4-12 weeks\n🇬🇧 English (IELTS/TOEFL): 4-8 weeks";
    }
    
    // ===== APPLICATION PROCESS =====
    if(q.includes('how to apply') || q.includes('application process') || q.includes('apply for')) {
        return "📝 How to Apply Through KHARY Global EDU:\n\n1️⃣ Browse universities on our website\n2️⃣ Contact us with your preferred country/program\n3️⃣ Submit your documents\n4️⃣ Our team reviews and guides you\n5️⃣ Receive admission letter\n6️⃣ Apply for visa with our assistance\n\n✅ FREE consultation! Contact us to start.";
    }
    
    // ===== CONTACT =====
    if(q.includes('contact') || q.includes('email') || q.includes('whatsapp') || q.includes('phone') || q.includes('reach') || q.includes('call')) {
        return "📞 Contact KHARY Global EDU:\n\n✉️ Email: kharyglobal@gmail.com\n💬 WhatsApp: +86 135 2246 4910\n📱 WeChat: kharyglobal\n\n📅 Free Consultation Available!";
    }
    
    // ===== GREETINGS =====
    if(q.includes('hello') || q.includes('hi') || q.includes('hey') || q.includes('greetings')) {
        return "👋 Hello! Welcome to KHARY Global EDU. How can I help you with your study abroad journey today? I can assist with scholarships, universities, fees, visas, and more!";
    }
    
    if(q.includes('thank')) {
        return "🙏 You're welcome! I'm glad I could help. Feel free to ask if you have any other questions about studying in Asia!";
    }
    
    if(q.includes('bye') || q.includes('goodbye')) {
        return "👋 Goodbye! Feel free to come back anytime you need assistance with your study abroad plans. Have a great day!";
    }
    
    // ===== HELP =====
    if(q.includes('help') || q.includes('what can you do') || q.includes('capabilities')) {
        return "🤖 I can help you with:\n\n📚 Universities & Programs\n💰 Scholarships & Funding\n📝 Application Process\n🌏 Country Information (China, Singapore, Malaysia, Japan, Korea)\n💵 Fees & Living Costs\n🎫 Visa Guidance\n🏠 Housing & Part-time Jobs\n📅 Deadlines & Requirements\n🗣️ Language Courses\n\nWhat would you like to know?";
    }
    
    // ===== DEFAULT RESPONSE with context =====
    return "🤖 I'm KHARY AI Assistant. I can help with:\n\n📚 Universities & Programs\n💰 Scholarships & Funding\n📝 Application Process\n🌏 Country Information\n💵 Fees & Living Costs\n🎫 Visa Guidance\n🏠 Housing & Part-time Jobs\n📅 Deadlines & Requirements\n🗣️ Language Courses\n\nWhat would you like to know? Just type your question or click one of the popular questions above!" + context;
}
    
    // Send message function
    function sendMessage() {
        const userMessage = chatInput.value.trim();
        if(!userMessage) return;
        
        addMessage(userMessage, true);
        chatInput.value = '';
        
        setTimeout(() => {
            const answer = getAnswer(userMessage);
            addMessage(answer, false);
        }, 400);
    }
    
    if(sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if(chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') sendMessage();
        });
    }
    
    // Quick questions mapping (30+ questions)
    const quickQuestions = {
        'scholarships': 'What scholarships are available?',
        'china': 'Tell me about studying in China',
        'singapore': 'Tell me about studying in Singapore',
        'malaysia': 'Tell me about studying in Malaysia',
        'japan': 'Tell me about studying in Japan',
        'korea': 'Tell me about studying in Korea',
        'fees': 'What are tuition fees?',
        'livingcost': 'What is the living cost?',
        'bachelor': 'How long is Bachelor degree?',
        'master': 'How long is Master degree?',
        'phd': 'How long is PhD program?',
        'requirements': 'What are admission requirements?',
        'documents': 'What documents are required?',
        'deadlines': 'What are application deadlines?',
        'visa': 'Tell me about student visa process',
        'parttime': 'Can I work part-time while studying?',
        'housing': 'Tell me about accommodation options',
        'csc': 'Tell me about CSC Scholarship China',
        'kgsp': 'Tell me about KGSP Scholarship Korea',
        'mext': 'Tell me about MEXT Scholarship Japan',
        'asean': 'Tell me about ASEAN Scholarship Singapore',
        'ielts': 'What is IELTS requirement?',
        'toefl': 'What is TOEFL requirement?',
        'apply': 'How to apply to universities?',
        'contact': 'How can I contact you?',
        'intake': 'What are intake seasons?',
        'hsktest': 'Tell me about HSK test',
        'jlpt': 'Tell me about JLPT test',
        'topik': 'Tell me about TOPIK test',
        'language': 'Tell me about language courses',
        'health': 'Tell me about health insurance'
    };
    
    document.querySelectorAll('.khary-quick-q').forEach(btn => {
        btn.addEventListener('click', () => {
            const qType = btn.getAttribute('data-q');
            const question = quickQuestions[qType] || qType;
            chatInput.value = question;
            sendMessage();
        });
    });
    
    // Auto-add FontAwesome if missing
    if(!document.querySelector('link[href*="font-awesome"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css';
        document.head.appendChild(link);
    }
})();