// static/csca_data.js
const cscaData = {
    overview: {
        fullName: "Chinese Scholastic Council Examination (CSCA)",
        alsoKnown: "Chinese University Entrance Examination for International Students",
        purpose: "Standardized entrance exam for international students applying to Chinese universities",
        website: "www.csca.cn"
    },
    examStructure: {
        subjects: [
            { name: "Chinese Language", score: 150, duration: "120 min", description: "Reading, writing, listening comprehension" },
            { name: "Mathematics", score: 150, duration: "120 min", description: "Algebra, geometry, calculus basics" },
            { name: "English", score: 100, duration: "90 min", description: "Reading, grammar, writing" },
            { name: "Comprehensive", score: 200, duration: "150 min", description: "Science or Humanities based on major" }
        ],
        totalScore: 600,
        passingScore: 360
    },
    testDates: [
        { session: "Spring", date: "March 15-20", registrationDeadline: "January 31", results: "April 30" },
        { session: "Fall", date: "September 10-15", registrationDeadline: "July 31", results: "October 31" }
    ],
    fee: {
        domestic: "¥500",
        international: "$80 USD"
    },
    universities: [
        { name: "Tsinghua University", requiredScore: 520, city: "Beijing", type: "C9 League" },
        { name: "Peking University", requiredScore: 510, city: "Beijing", type: "C9 League" },
        { name: "Fudan University", requiredScore: 500, city: "Shanghai", type: "C9 League" },
        { name: "Shanghai Jiao Tong University", requiredScore: 500, city: "Shanghai", type: "C9 League" },
        { name: "Zhejiang University", requiredScore: 490, city: "Hangzhou", type: "C9 League" },
        { name: "University of Science and Technology of China", requiredScore: 490, city: "Hefei", type: "C9 League" },
        { name: "Nanjing University", requiredScore: 480, city: "Nanjing", type: "C9 League" },
        { name: "Wuhan University", requiredScore: 470, city: "Wuhan", type: "Double First Class" },
        { name: "Harbin Institute of Technology", requiredScore: 470, city: "Harbin", type: "C9 League" },
        { name: "Xi'an Jiaotong University", requiredScore: 470, city: "Xi'an", type: "C9 League" },
        { name: "Sun Yat-sen University", requiredScore: 460, city: "Guangzhou", type: "Double First Class" },
        { name: "Huazhong University of Science and Technology", requiredScore: 460, city: "Wuhan", type: "Double First Class" },
        { name: "Tianjin University", requiredScore: 450, city: "Tianjin", type: "Double First Class" },
        { name: "Sichuan University", requiredScore: 440, city: "Chengdu", type: "Double First Class" },
        { name: "Beihang University", requiredScore: 450, city: "Beijing", type: "Double First Class" },
        { name: "Beijing Institute of Technology", requiredScore: 440, city: "Beijing", type: "Double First Class" },
        { name: "Shandong University", requiredScore: 430, city: "Jinan", type: "Double First Class" },
        { name: "South China University of Technology", requiredScore: 430, city: "Guangzhou", type: "Double First Class" }
    ],
    preparationTips: [
        "Start preparing 6 months before exam",
        "Take mock tests regularly",
        "Focus on Chinese language and math",
        "Review past exam papers",
        "Join study groups",
        "Use CSCA official preparation materials"
    ],
    documents: [
        "Valid passport",
        "High school diploma (notarized)",
        "Academic transcripts",
        "Passport photos (2-inch, white background)",
        "Application fee payment receipt",
        "Health certificate"
    ]
};