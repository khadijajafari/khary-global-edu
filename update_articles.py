import sqlite3

conn = sqlite3.connect('applications.db')
c = conn.cursor()

# ==================== ARTICLE 1: CHINA - ULTRA PREMIUM DETAILED ====================
china_content = '''
<h1>🇨🇳 The Complete Guide to Studying in China: Top Universities, CSC Scholarship, Application Process & More</h1>

<div class="info-box">
<h3>📊 Quick Overview</h3>
<ul>
<li>🏛️ 147 "Double First Class" Universities | 2,000+ Total Universities</li>
<li>🌏 500,000+ International Students from 190+ Countries</li>
<li>💰 Tuition: ¥18,000-45,000/year ($2,500-6,200 USD)</li>
<li>🏠 Living Cost: ¥4,500-8,000/month ($620-1,100 USD)</li>
<li>📚 Chinese/English Medium Instruction</li>
<li>🎓 280+ CSC Scholarship Universities | 500+ English Programs</li>
</ul>
</div>

<h2>📖 Table of Contents</h2>
<ul>
<li>1. Why Study in China? – The World's Fastest-Growing Education Hub</li>
<li>2. Top 50 Universities in China (C9 League, Project 985, Double First Class)</li>
<li>3. Detailed University Profiles (Tsinghua, Peking, Fudan, SJTU, ZJU + 20 more)</li>
<li>4. Complete Admission Requirements (Undergraduate, Graduate, PhD)</li>
<li>5. CSC Scholarship Guide – Full Tuition + Monthly Stipend</li>
<li>6. Tuition Fees by University and Program</li>
<li>7. Cost of Living in Major Cities (Beijing, Shanghai, Guangzhou, Chengdu)</li>
<li>8. Student Visa Process (X1 and X2 Visa)</li>
<li>9. Student Life & Culture – What to Expect</li>
<li>10. Career Opportunities After Graduation</li>
<li>11. Frequently Asked Questions</li>
<li>12. City Guide: Beijing, Shanghai, Guangzhou, Hangzhou, Nanjing, Chengdu</li>
</ul>

<h2>1. Why Study in China? – The World's Fastest-Growing Education Hub</h2>
<p>China has emerged as the world's leading destination for international education, surpassing the US and UK in international student numbers. With over 500,000 international students from 190 countries, China offers a unique blend of world-class education, rich cultural heritage, and unprecedented economic opportunities.</p>

<h3>1.1 World-Class Education System</h3>
<p>China's "Double First Class" initiative has invested over $10 billion to develop 147 universities into world-class institutions. Chinese universities now rank among the world's best, with Tsinghua (#16), Peking (#17), and Fudan (#34) leading the way. Research output in STEM, AI, and engineering is now the highest in the world.</p>

<h3>1.2 Affordable Excellence</h3>
<p>Compared to Western countries, studying in China offers exceptional value. Tuition at top universities is 60-80% cheaper than equivalent US or UK institutions, while maintaining world-class standards. The CSC Scholarship further reduces costs, covering full tuition and providing a generous monthly stipend.</p>

<h3>1.3 Career Opportunities</h3>
<p>China is the world's second-largest economy and the global leader in AI, 5G, e-commerce, and renewable energy. Graduates from Chinese universities are highly sought after by multinational corporations, with China now the top destination for foreign direct investment. Knowledge of Chinese language and culture is a significant career advantage.</p>

<h3>1.4 Rich Cultural Heritage</h3>
<p>With 5,000 years of history, China offers an unparalleled cultural experience. From the Great Wall and Forbidden City to modern megacities like Shanghai and Shenzhen, students experience both ancient traditions and cutting-edge innovation.</p>

<h2>2. Top 50 Universities in China</h2>

<h3>The C9 League – China's Ivy League</h3>
<p>The C9 League consists of China's top 9 universities, receiving the most government funding and producing the nation's top researchers and leaders.</p>

<h4>2.1 Tsinghua University (清华大学)</h4>
<p><strong>Ranking:</strong> #1 China, #16 World, #1 in Asia for Engineering</p>
<p><strong>Location:</strong> Beijing (Haidian District)</p>
<p><strong>Established:</strong> 1911</p>
<p><strong>Student Population:</strong> 50,000+ (12% international)</p>
<p><strong>Motto:</strong> "Self-Discipline and Social Commitment"</p>
<p><strong>Faculties:</strong> 20 colleges, 59 departments</p>
<p><strong>Top Programs:</strong></p>
<ul>
<li>Engineering: #1 in China, #12 World (Civil, Mechanical, Electrical, Chemical, Environmental)</li>
<li>Computer Science: #1 in China, #15 World (AI, Data Science, Cybersecurity)</li>
<li>Business: #1 in China, #25 World (Tsinghua SEM, MBA #1 in Asia)</li>
<li>Architecture: #1 in China, #8 World</li>
<li>Economics: #2 in China, #30 World</li>
<li>Law: #2 in China, #40 World</li>
<li>Medicine: #5 in China, #100 World</li>
</ul>
<p><strong>Research Excellence:</strong> 40 national key laboratories, 5 million+ sqm research facilities. Home to China's leading AI research center and quantum computing laboratory.</p>
<p><strong>Campus:</strong> 980-acre campus with 12 libraries (5.5 million volumes), Olympic-sized pool, 8 gyms, 24 student restaurants, and the iconic Schwarzman College (global leaders program).</p>
<p><strong>Notable Alumni:</strong> 14 Chinese Presidents/Prime Ministers, Nobel Laureates, CEOs of major Chinese tech companies (Alibaba, Tencent, Baidu founders).</p>
<p><strong>International Partnerships:</strong> 300+ partner universities including MIT, Harvard, Cambridge, ETH Zurich.</p>
<p><strong>Acceptance Rate:</strong> 10-15% (undergraduate), 5-10% (graduate)</p>
<p><strong>Tuition:</strong> ¥26,000-40,000/year ($3,600-5,500 USD)</p>
<p><strong>Scholarships:</strong> CSC Scholarship, Tsinghua Scholarship (50-100% tuition), Beijing Government Scholarship</p>

<h4>2.2 Peking University (北京大学)</h4>
<p><strong>Ranking:</strong> #2 China, #17 World, #1 in Asia for Humanities & Social Sciences</p>
<p><strong>Location:</strong> Beijing (Haidian District)</p>
<p><strong>Established:</strong> 1898</p>
<p><strong>Student Population:</strong> 45,000+ (15% international)</p>
<p><strong>Motto:</strong> "Patriotism, Progress, Democracy, Science"</p>
<p><strong>Faculties:</strong> 30 colleges, 12 departments</p>
<p><strong>Top Programs:</strong></p>
<ul>
<li>Medicine: #1 in China (Peking University Health Science Center)</li>
<li>Law: #1 in China, #20 World (China's most prestigious law school)</li>
<li>Economics: #1 in China, #25 World</li>
<li>Chinese Literature: #1 in China</li>
<li>Philosophy: #1 in China</li>
<li>Political Science: #1 in China</li>
<li>Business: #3 in China (Guanghua School of Management)</li>
<li>Computer Science: #5 in China</li>
</ul>
<p><strong>Research Centers:</strong> 7 national key laboratories, 100+ research institutes including the Institute of Molecular Medicine and the Center for Chinese Classics.</p>
<p><strong>Campus:</strong> The "Yan Yuan" campus is considered China's most beautiful university campus, featuring traditional Chinese architecture, Weiming Lake, and the famous Boya Tower. 11 libraries with 8 million volumes.</p>
<p><strong>Notable Alumni:</strong> 5 Chinese Presidents/Prime Ministers, Nobel Laureate (Tu Youyou), and leaders across politics, academia, and business.</p>
<p><strong>Tuition:</strong> ¥24,000-38,000/year ($3,300-5,200 USD)</p>
<p><strong>Scholarships:</strong> Peking University Scholarship, CSC Scholarship, Beijing Government Scholarship</p>

<h4>2.3 Fudan University (复旦大学)</h4>
<p><strong>Ranking:</strong> #3 China, #34 World</p>
<p><strong>Location:</strong> Shanghai (Yangpu District)</p>
<p><strong>Established:</strong> 1905</p>
<p><strong>Student Population:</strong> 40,000+ (14% international)</p>
<p><strong>Motto:</strong> "Rich in Knowledge, Tenacious of Purpose, Inquiring with Earnestness, Reflecting with Self-practice"</p>
<p><strong>Top Programs:</strong></p>
<ul>
<li>Business: #2 in China (Fudan School of Management, Top 50 globally)</li>
<li>Medicine: #3 in China (Fudan Shanghai Medical College)</li>
<li>Economics: #3 in China</li>
<li>Journalism: #1 in China</li>
<li>International Relations: #2 in China</li>
<li>Pharmacy: #3 in China</li>
<li>Computer Science: #10 in China</li>
</ul>
<p><strong>Campus:</strong> 3 campuses in Shanghai: Handan (main), Jiangwan, Fenglin. State-of-the-art facilities including the 1,200-bed Fudan University Shanghai Cancer Center.</p>
<p><strong>Industry Connections:</strong> Located in Yangpu District, Shanghai's innovation hub, with close ties to Shanghai Stock Exchange, international banks, and Fortune 500 companies.</p>
<p><strong>Tuition:</strong> ¥22,000-36,000/year ($3,000-5,000 USD)</p>
<p><strong>Scholarships:</strong> Fudan University Scholarship, Shanghai Government Scholarship, CSC Scholarship</p>

<h4>2.4 Shanghai Jiao Tong University (上海交通大学)</h4>
<p><strong>Ranking:</strong> #4 China, #46 World</p>
<p><strong>Location:</strong> Shanghai (Minhang District)</p>
<p><strong>Established:</strong> 1896</p>
<p><strong>Student Population:</strong> 42,000+ (13% international)</p>
<p><strong>Top Programs:</strong></p>
<ul>
<li>Engineering: #2 in China (Mechanical, Electrical, Naval Architecture, Materials)</li>
<li>Computer Science: #3 in China (AI, Robotics, Software Engineering)</li>
<li>Business: #4 in China (Antai College of Economics and Management)</li>
<li>Medicine: #4 in China (Shanghai Jiao Tong University School of Medicine)</li>
<li>Naval Architecture: #1 in China</li>
<li>Biomedical Engineering: #2 in China</li>
</ul>
<p><strong>Research Excellence:</strong> 16 national key laboratories, 2 national engineering research centers. Home to China's leading robotics and AI research groups.</p>
<p><strong>Campus:</strong> 5,000-acre campus (largest in Shanghai), 12 libraries, 5 museums, 3 hospitals, Olympic sports facilities.</p>
<p><strong>Industry Connections:</strong> Strong partnerships with Tesla, General Motors, Intel, Microsoft, and Chinese tech giants.</p>
<p><strong>Tuition:</strong> ¥24,000-38,000/year ($3,300-5,200 USD)</p>

<h4>2.5 Zhejiang University (浙江大学)</h4>
<p><strong>Ranking:</strong> #5 China, #42 World</p>
<p><strong>Location:</strong> Hangzhou, Zhejiang</p>
<p><strong>Established:</strong> 1897</p>
<p><strong>Student Population:</strong> 48,000+ (12% international)</p>
<p><strong>Top Programs:</strong></p>
<ul>
<li>Agricultural Science: #1 in China</li>
<li>Computer Science: #4 in China</li>
<li>Engineering: #4 in China (Chemical, Mechanical, Civil)</li>
<li>Food Science: #1 in China</li>
<li>Optics: #1 in China</li>
<li>Business: #5 in China</li>
</ul>
<p><strong>Campus:</strong> 7 campuses across Hangzhou, including the beautiful Zijingang campus. Located in Hangzhou, one of China's most beautiful cities, home to Alibaba headquarters.</p>
<p><strong>Research Centers:</strong> 14 national key laboratories, including the State Key Laboratory of CAD&CG (computer graphics).</p>
<p><strong>Tuition:</strong> ¥22,000-35,000/year ($3,000-4,800 USD)</p>

<h3>More Top 30 Universities (6-30)</h3>
<ul>
<li><strong>2.6 University of Science and Technology of China (USTC):</strong> #6 China, #93 World – Physics, Chemistry, Quantum Computing</li>
<li><strong>2.7 Nanjing University:</strong> #7 China, #95 World – Humanities, Geology, Chinese Language</li>
<li><strong>2.8 Wuhan University:</strong> #8 China, #157 World – Law, Economics, Remote Sensing, Cherry Blossoms Campus</li>
<li><strong>2.9 Harbin Institute of Technology (HIT):</strong> #9 China, #260 World – Aerospace, Robotics, Mechanical Engineering</li>
<li><strong>2.10 Xi'an Jiaotong University:</strong> #10 China, #290 World – Electrical Engineering, Management, Energy</li>
<li><strong>2.11 Sun Yat-sen University:</strong> #11 China, #159 World – Medicine, Business, Marine Science, Guangzhou</li>
<li><strong>2.12 Beijing Normal University:</strong> #12 China, #251 World – Education, Psychology, Chinese Language</li>
<li><strong>2.13 Tianjin University:</strong> #13 China, #334 World – Chemical Engineering, Architecture, Civil Engineering</li>
<li><strong>2.14 Sichuan University:</strong> #14 China, #355 World – Stomatology (Dentistry), Pharmacy, Chinese Medicine</li>
<li><strong>2.15 Shandong University:</strong> #15 China, #403 World – Chinese Culture, Marine Biology, Mathematics</li>
<li><strong>2.16 Tongji University:</strong> #16 China, #211 World – Architecture, Civil Engineering, Urban Planning, Shanghai</li>
<li><strong>2.17 Beihang University (BUAA):</strong> #17 China, #251 World – Aerospace Engineering, Computer Science, Beijing</li>
<li><strong>2.18 East China Normal University:</strong> #18 China, #301 World – Education, Chinese Language, Psychology, Shanghai</li>
<li><strong>2.19 South China University of Technology:</strong> #19 China, #341 World – Chemical Engineering, Food Science, Guangzhou</li>
<li><strong>2.20 University of Electronic Science and Technology of China (UESTC):</strong> #20 China, #371 World – Electronics, Communication, AI, Chengdu</li>
<li><strong>2.21 Dalian University of Technology:</strong> #21 China, #401 World – Mechanical Engineering, Naval Architecture, Dalian</li>
<li><strong>2.22 Northwestern Polytechnical University:</strong> #22 China, #431 World – Aeronautics, Astronautics, Marine Engineering, Xi'an</li>
<li><strong>2.23 China Agricultural University:</strong> #23 China, #451 World – Agriculture, Food Science, Biotechnology, Beijing</li>
<li><strong>2.24 Lanzhou University:</strong> #24 China, #481 World – Chemistry, Ecology, Arid Zone Research, Lanzhou</li>
<li><strong>2.25 Hunan University:</strong> #25 China, #511 World – Mechanical Engineering, Chemistry, Business, Changsha</li>
<li><strong>2.26 Chongqing University:</strong> #26 China, #541 World – Civil Engineering, Mechanical Engineering, Architecture</li>
<li><strong>2.27 Jilin University:</strong> #27 China, #571 World – Chemistry, Medicine, Automotive Engineering, Changchun</li>
<li><strong>2.28 Ocean University of China:</strong> #28 China, #601 World – Marine Science, Fisheries, Oceanography, Qingdao</li>
<li><strong>2.29 Northeastern University (China):</strong> #29 China, #631 World – Computer Science, Software Engineering, Automation, Shenyang</li>
<li><strong>2.30 Soochow University:</strong> #30 China, #651 World – Medicine, Materials Science, Textile Engineering, Suzhou</li>
</ul>

<h3>Double First Class Universities (31-50)</h3>
<ul>
<li>31. Nankai University (Tianjin)</li>
<li>32. Xiamen University (Xiamen)</li>
<li>33. Southeast University (Nanjing)</li>
<li>34. Central South University (Changsha)</li>
<li>35. Huazhong University of Science and Technology (Wuhan)</li>
<li>36. Wuhan University of Technology (Wuhan)</li>
<li>37. Nanjing University of Aeronautics and Astronautics (Nanjing)</li>
<li>38. Nanjing University of Science and Technology (Nanjing)</li>
<li>39. Beijing University of Technology (Beijing)</li>
<li>40. Beijing University of Chemical Technology (Beijing)</li>
<li>41. Beijing Forestry University (Beijing)</li>
<li>42. Beijing University of Posts and Telecommunications (Beijing)</li>
<li>43. Beijing Jiaotong University (Beijing)</li>
<li>44. China University of Geosciences (Beijing/Wuhan)</li>
<li>45. China University of Petroleum (Beijing/Qingdao)</li>
<li>46. China University of Mining and Technology (Beijing/Xuzhou)</li>
<li>47. East China University of Science and Technology (Shanghai)</li>
<li>48. Shanghai University (Shanghai)</li>
<li>49. Shanghai University of Finance and Economics (Shanghai)</li>
<li>50. Central University of Finance and Economics (Beijing)</li>
</ul>

<h2>3. Detailed University Profiles (Top 10 In-Depth)</h2>

<h3>3.1 Tsinghua University – The MIT of China</h3>
<p><strong>Schools and Departments:</strong></p>
<ul>
<li><strong>School of Information Science and Technology:</strong> China's #1 CS program, research in AI, Big Data, Cybersecurity</li>
<li><strong>School of Economics and Management (SEM):</strong> AACSB, EQUIS, AMBA accredited. MBA #1 in Asia</li>
<li><strong>School of Medicine:</strong> Collaborative with McGovern Institute, strong in neuroscience and biomedical engineering</li>
<li><strong>School of Law:</strong> China's premier law school, strong in international and commercial law</li>
<li><strong>School of Public Policy and Management:</strong> Training China's future leaders</li>
<li><strong>Academy of Arts & Design:</strong> #1 in China for design, architecture, fine arts</li>
</ul>

<p><strong>Research Excellence:</strong></p>
<ul>
<li>40 National Key Laboratories</li>
<li>5.2 billion RMB annual research funding</li>
<li>500+ patents filed annually</li>
<li>Home to China's most powerful supercomputer (Tianhe-2)</li>
<li>National Laboratory for Information Science and Technology</li>
</ul>

<p><strong>International Programs:</strong></p>
<ul>
<li><strong>Schwarzman Scholars:</strong> Fully-funded global leaders program modeled after Rhodes Scholarship</li>
<li><strong>Global Summer School:</strong> 300+ international students annually</li>
<li><strong>Dual Degree Programs:</strong> with MIT, Johns Hopkins, University of Washington</li>
</ul>

<h3>3.2 Peking University – The Harvard of China</h3>
<p><strong>Schools and Departments:</strong></p>
<ul>
<li><strong>Peking University Health Science Center:</strong> China's #1 medical school, 8 affiliated hospitals</li>
<li><strong>Guanghua School of Management:</strong> China's #2 business school, strong in finance and entrepreneurship</li>
<li><strong>School of Law:</strong> China's #1 law school, 20 research centers, international law focus</li>
<li><strong>School of Economics:</strong> China's premier economics program, home to China's leading economists</li>
<li><strong>School of International Studies:</strong> Top Asian studies program, language and culture immersion</li>
</ul>

<p><strong>Cultural Heritage:</strong></p>
<ul>
<li>Weiming Lake – 600-year-old lake, heart of campus life</li>
<li>Boya Tower – Iconic landmark, symbol of PKU</li>
<li>12 libraries, 8 million volumes, East Asia's largest academic library</li>
<li>University museums: History, Archaeology, and Nature</li>
</ul>

<h2>4. Complete Admission Requirements</h2>

<h3>Undergraduate Programs</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;">
<th>Program Type</th>
<th>Academic Requirements</th>
<th>Language Requirements</th>
<th>Additional Requirements</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Chinese-Taught Programs</strong></td>
<td>High School Diploma (85%+), SAT 1400+/ACT 30+, A-Levels (AAB), IB (38+)</td>
<td>HSK Level 4 (minimum 180) or Level 5 (recommended)</td>
<td>Personal Statement, 2 Recommendation Letters, Interview</td>
</tr>
<tr>
<td><strong>English-Taught Programs</strong></td>
<td>High School Diploma (85%+), SAT 1400+/ACT 30+</td>
<td>IELTS 6.5 (min 6.0) or TOEFL 90+</td>
<td>Personal Statement, 2 Recommendation Letters, Interview</td>
</tr>
<tr>
<td><strong>Medical Programs (MBBS)</strong></td>
<td>High School Diploma (85%+), Biology, Chemistry, Physics</td>
<td>IELTS 6.5 or HSK 4</td>
<td>Medical Examination, Interview, Portfolio</td>
</tr>
</tbody>
</table>

<h3>Graduate Programs (Master's & PhD)</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;">
<th>Program Level</th>
<th>Academic Requirements</th>
<th>Language Requirements</th>
<th>Research Requirements</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Master's by Coursework</strong></td>
<td>Bachelor's Degree (3.5/4.0 GPA), Relevant field</td>
<td>IELTS 6.5/TOEFL 90 or HSK 5</td>
<td>Work Experience (for MBA), Statement of Purpose</td>
</tr>
<tr>
<td><strong>Master's by Research</strong></td>
<td>Bachelor's Degree (3.3/4.0 GPA), Research background</td>
<td>IELTS 6.5/TOEFL 90 or HSK 5</td>
<td>Research Proposal (2,000 words), Publications (recommended)</td>
</tr>
<tr>
<td><strong>PhD</strong></td>
<td>Master's Degree (3.5/4.0 GPA), Excellent academic record</td>
<td>IELTS 7.0/TOEFL 100 or HSK 6</td>
<td>Research Proposal, Publications, Interview with supervisor</td>
</tr>
</tbody>
</table>

<h2>5. CSC Scholarship Guide – Full Tuition + Monthly Stipend</h2>

<h3>What is the CSC Scholarship?</h3>
<p>The Chinese Government Scholarship (CSC) is the most prestigious and comprehensive scholarship for international students, funded by the Chinese Ministry of Education. Over 280 Chinese universities participate, covering 100% of tuition and providing generous living stipends.</p>

<h3>Scholarship Benefits</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;">
<th>Category</th>
<th>Coverage</th>
</tr>
</thead>
<tbody>
<tr><td><strong>Tuition</strong></td><td>100% tuition waiver (full duration of program)</td></tr>
<tr><td><strong>Accommodation</strong></td><td>Free on-campus dormitory or monthly accommodation allowance</td></tr>
<tr><td><strong>Monthly Stipend</strong></td><td>Undergraduate: ¥2,500 | Master's: ¥3,000 | PhD: ¥3,500</td></tr>
<tr><td><strong>Medical Insurance</strong></td><td>Comprehensive medical insurance coverage</td></tr>
<tr><td><strong>Language Training</strong></td><td>1-year Chinese language training (if needed)</td></tr>
</tbody>
</table>

<h3>Types of CSC Scholarships</h3>
<ul>
<li><strong>Type A – Bilateral Program:</strong> Apply through Chinese embassy in your home country. Deadline: January-March. Each country has 2-20 quotas.</li>
<li><strong>Type B – Chinese University Program:</strong> Apply directly to universities. Deadline: February-April. More flexible, 280+ participating universities.</li>
<li><strong>Type C – Special Programs:</strong> EU Program, AUN Program, Great Wall Program, WMO Program.</li>
</ul>

<h3>Application Timeline</h3>
<ul>
<li><strong>January-February:</strong> Prepare documents, contact potential supervisors</li>
<li><strong>March-April:</strong> Submit online application, university recommendation</li>
<li><strong>May-June:</strong> University review, CSC final selection</li>
<li><strong>July-August:</strong> Results announced, admission letters sent</li>
<li><strong>September:</strong> Arrive in China, registration</li>
</ul>

<h2>6. Tuition Fees by University</h2>

<h3>Top Tier Universities (C9 League)</h3>
<ul>
<li>Tsinghua: ¥26,000-40,000/year</li>
<li>Peking: ¥24,000-38,000/year</li>
<li>Fudan: ¥22,000-36,000/year</li>
<li>SJTU: ¥24,000-38,000/year</li>
<li>Zhejiang: ¥22,000-35,000/year</li>
<li>USTC: ¥20,000-32,000/year</li>
<li>Nanjing: ¥20,000-34,000/year</li>
<li>Wuhan: ¥20,000-33,000/year</li>
<li>HIT: ¥18,000-30,000/year</li>
<li>Xi'an Jiaotong: ¥18,000-32,000/year</li>
</ul>

<h3>MBBS (Medicine) Programs</h3>
<ul>
<li>Peking University Medical: ¥45,000/year</li>
<li>Fudan University Medical: ¥42,000/year</li>
<li>SJTU Medical: ¥44,000/year</li>
<li>Wuhan University Medical: ¥35,000/year</li>
<li>Sichuan University Medical: ¥38,000/year</li>
</ul>

<h3>MBA Programs</h3>
<ul>
<li>Tsinghua MBA: ¥368,000 total (2 years)</li>
<li>Peking Guanghua MBA: ¥328,000 total</li>
<li>Fudan MBA: ¥339,000 total</li>
<li>SJTU Antai MBA: ¥358,000 total</li>
</ul>

<h2>7. Cost of Living in Major Cities</h2>

<h3>Beijing (Tsinghua, Peking, Beihang, BNU)</h3>
<ul>
<li>Accommodation: ¥800-2,500/month</li>
<li>Food: ¥1,500-2,500/month</li>
<li>Transport: ¥200-300/month</li>
<li>Utilities: ¥300-500/month</li>
<li><strong>Total: ¥4,500-8,000/month ($620-1,100 USD)</strong></li>
</ul>

<h3>Shanghai (Fudan, SJTU, Tongji, ECNU)</h3>
<ul>
<li>Accommodation: ¥1,000-3,000/month</li>
<li>Food: ¥1,800-2,800/month</li>
<li>Transport: ¥200-300/month</li>
<li>Utilities: ¥400-600/month</li>
<li><strong>Total: ¥5,000-9,000/month ($690-1,240 USD)</strong></li>
</ul>

<h3>Guangzhou (Sun Yat-sen, SCUT)</h3>
<ul>
<li>Accommodation: ¥600-1,800/month</li>
<li>Food: ¥1,200-2,000/month</li>
<li>Transport: ¥150-250/month</li>
<li><strong>Total: ¥3,500-6,500/month ($480-900 USD)</strong></li>
</ul>

<h3>Chengdu (Sichuan, UESTC)</h3>
<ul>
<li>Accommodation: ¥500-1,500/month</li>
<li>Food: ¥1,000-1,800/month</li>
<li>Transport: ¥100-200/month</li>
<li><strong>Total: ¥3,000-5,500/month ($410-760 USD)</strong></li>
</ul>

<h2>8. Student Visa Process (X1 and X2 Visa)</h2>

<h3>X1 Visa (Long-term, >180 days)</h3>
<p><strong>Requirements:</strong></p>
<ul>
<li>Valid passport (6+ months validity)</li>
<li>JW201/JW202 form (from university)</li>
<li>Admission letter</li>
<li>Physical examination record (Foreigner Physical Examination Form)</li>
<li>2 passport photos (33x48mm, white background)</li>
<li>Bank statements (RMB 100,000+ for one year)</li>
<li>Police clearance certificate</li>
</ul>
<p><strong>Processing time:</strong> 4-7 working days</p>
<p><strong>Visa fee:</strong> $140-200 (varies by country)</p>

<h3>X2 Visa (Short-term, <180 days)</h3>
<p><strong>Requirements:</strong></p>
<ul>
<li>Valid passport</li>
<li>Admission letter</li>
<li>Proof of financial support</li>
</ul>
<p><strong>Processing time:</strong> 4-5 working days</p>

<h3>Step-by-Step Process</h3>
<ol>
<li><strong>Step 1:</strong> Receive admission letter and JW201/JW202 form from university</li>
<li><strong>Step 2:</strong> Complete medical examination (authorized hospital)</li>
<li><strong>Step 3:</strong> Submit application at Chinese embassy/consulate</li>
<li><strong>Step 4:</strong> Receive visa (4-7 working days)</li>
<li><strong>Step 5:</strong> Travel to China</li>
<li><strong>Step 6:</strong> Apply for Residence Permit within 30 days of arrival (at local Public Security Bureau)</li>
</ol>

<h2>9. Student Life & Culture</h2>

<h3>Festivals and Holidays</h3>
<ul>
<li><strong>Chinese New Year (Spring Festival):</strong> January/February, 7-day national holiday, largest celebration</li>
<li><strong>Mid-Autumn Festival:</strong> September/October, mooncakes, family gatherings</li>
<li><strong>Dragon Boat Festival:</strong> May/June, dragon boat races, zongzi (sticky rice dumplings)</li>
<li><strong>National Day:</strong> October 1, 7-day holiday, fireworks and parades</li>
<li><strong>Lantern Festival:</strong> February, lantern displays, tangyuan (sweet rice balls)</li>
</ul>

<h3>Student Activities</h3>
<ul>
<li><strong>Clubs and Societies:</strong> 100+ clubs per university: music, dance, sports, chess, calligraphy, martial arts</li>
<li><strong>Sports:</strong> Basketball (most popular), badminton, table tennis, soccer, swimming, martial arts (Tai Chi, Kung Fu)</li>
<li><strong>Cultural Exchange:</strong> International student events, language exchange partners, Chinese cooking classes</li>
<li><strong>Travel:</strong> Explore Great Wall, Forbidden City, Terracotta Army, Zhangjiajie (Avatar mountains), Li River, Huangshan</li>
</ul>

<h2>10. Career Opportunities After Graduation</h2>

<h3>Top Employers Hiring Chinese University Graduates</h3>
<ul>
<li><strong>Technology:</strong> Huawei, Alibaba, Tencent, Baidu, Xiaomi, DJI, ByteDance (TikTok)</li>
<li><strong>Automotive:</strong> BYD, Geely, NIO, Xpeng, Tesla China</li>
<li><strong>Finance:</strong> ICBC, China Construction Bank, Agricultural Bank of China, Bank of China, Ping An Insurance</li>
<li><strong>Consulting:</strong> McKinsey, BCG, Bain, Deloitte, PwC, EY, KPMG</li>
<li><strong>Pharmaceutical:</strong> Fosun Pharma, WuXi AppTec, Sinopharm</li>
<li><strong>International:</strong> Microsoft, Google, Apple, Amazon, Intel, Qualcomm, Volkswagen, BMW</li>
</ul>

<h3>Average Starting Salaries</h3>
<ul>
<li>Computer Science/AI: ¥400,000-600,000/year ($55,000-82,000 USD)</li>
<li>Engineering: ¥300,000-450,000/year ($41,000-62,000 USD)</li>
<li>Business/Finance: ¥350,000-500,000/year ($48,000-68,000 USD)</li>
<li>Medicine: ¥500,000-800,000/year ($68,000-110,000 USD)</li>
<li>Research/Academia: ¥250,000-400,000/year ($34,000-55,000 USD)</li>
</ul>

<h2>11. Frequently Asked Questions</h2>

<h3>Q1: Can I work while studying in China?</h3>
<p>Yes, international students can work up to 20 hours/week with permission from university and immigration. Common jobs: English teaching, tutoring, internships at multinational companies.</p>

<h3>Q2: Do I need to learn Chinese?</h3>
<p>For English-taught programs, Chinese is not required. However, learning basic Chinese (HSK 3-4) greatly enhances daily life and career opportunities. Free Chinese language courses are often offered by universities.</p>

<h3>Q3: Is China safe for international students?</h3>
<p>Yes, China is one of the safest countries for international students. Universities have 24/7 security, and violent crime rates are extremely low. Female students feel safe walking alone at night.</p>

<h3>Q4: Can I stay in China after graduation?</h3>
<p>Yes, graduates can apply for the "Z" work visa or entrepreneurship visa. Many cities offer favorable policies for foreign graduates to start businesses or work in high-tech sectors.</p>

<h3>Q5: What is the weather like?</h3>
<p>Varies by region: Beijing has four distinct seasons (cold winters, hot summers). Shanghai is humid subtropical (mild winters, hot humid summers). Southern cities like Guangzhou are tropical (warm year-round).</p>

<h3>Q6: Can my family visit me?</h3>
<p>Yes, family members can apply for S1 (long-term) or S2 (short-term) family visit visas. Spouse and children can accompany on S1 visa with residence permit.</p>

<h3>Q7: What vaccinations are required?</h3>
<p>Recommended: Hepatitis B, Japanese Encephalitis, Rabies (if working with animals). Required: COVID-19 vaccination (may vary), Tuberculosis screening (for some countries).</p>

<h3>Q8: How do I open a bank account?</h3>
<p>Bring passport, student ID, residence permit to major banks: ICBC, Bank of China, China Construction Bank. Online banking and Alipay/WeChat Pay are essential for daily life.</p>

<h2>12. City Guide: Where to Study in China</h2>

<h3>Beijing – The Capital of Education</h3>
<p><strong>Universities:</strong> Tsinghua, Peking, Beihang, BNU, BIT</p>
<p><strong>Highlights:</strong> Forbidden City, Great Wall, 798 Art District, Houhai Lake</p>
<p><strong>Cost of Living:</strong> ¥5,000-8,000/month</p>

<h3>Shanghai – China's Financial Hub</h3>
<p><strong>Universities:</strong> Fudan, SJTU, Tongji, ECNU</p>
<p><strong>Highlights:</strong> The Bund, Oriental Pearl Tower, French Concession, Disneyland</p>
<p><strong>Cost of Living:</strong> ¥5,500-9,000/month</p>

<h3>Guangzhou – Southern Gateway</h3>
<p><strong>Universities:</strong> Sun Yat-sen, SCUT</p>
<p><strong>Highlights:</strong> Canton Tower, Shamian Island, Dim Sum, Canton Fair</p>
<p><strong>Cost of Living:</strong> ¥3,800-6,500/month</p>

<h3>Hangzhou – Paradise on Earth</h3>
<p><strong>Universities:</strong> Zhejiang University</p>
<p><strong>Highlights:</strong> West Lake, Alibaba HQ, Longjing Tea, Lingyin Temple</p>
<p><strong>Cost of Living:</strong> ¥4,000-6,500/month</p>

<h3>Chengdu – Land of Pandas</h3>
<p><strong>Universities:</strong> Sichuan University, UESTC</p>
<p><strong>Highlights:</strong> Panda Base, Sichuan Cuisine, Jinli Ancient Street, Leshan Giant Buddha</p>
<p><strong>Cost of Living:</strong> ¥3,000-5,500/month</p>

<h3>Wuhan – City of a Thousand Lakes</h3>
<p><strong>Universities:</strong> Wuhan University, HUST</p>
<p><strong>Highlights:</strong> Cherry Blossoms, Yellow Crane Tower, East Lake</p>
<p><strong>Cost of Living:</strong> ¥3,500-6,000/month</p>

<div class="info-box" style="background:#1E3A8A; color:white; text-align:center; padding:30px;">
<h2>🎓 Ready to Start Your China Journey?</h2>
<p>With world-class universities, affordable tuition, and generous scholarships, China offers an unparalleled study abroad experience. The CSC Scholarship, C9 League universities, and 500+ English-taught programs make China the smart choice for ambitious international students.</p>
<p><strong>Apply today and join 500,000+ international students who chose China!</strong></p>
<p>🇨🇳 Your future starts here. 🇨🇳</p>
</div>
'''

# Update Article 1 (China)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 1", (china_content,))
print("✅ Updated China article (ID 1)")

# ==================== ARTICLE 2: COMPLETE SCHOLARSHIP GUIDE - PREMIUM DESIGN ====================
scholarship_content = '''
<style>
.scholarship-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2D4FA8 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}
.scholarship-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: linear-gradient(135deg, #D4AF37, #F3D03E);
    color: #1E3A8A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.stat-number {
    font-size: 32px;
    font-weight: bold;
}
.scholarship-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #D4AF37;
    transition: transform 0.3s;
}
.scholarship-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(30,58,138,0.15);
}
.scholarship-title {
    color: #1E3A8A;
    font-size: 24px;
    margin-bottom: 15px;
    border-bottom: 2px solid #D4AF37;
    display: inline-block;
    padding-bottom: 5px;
}
.scholarship-details {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin: 15px 0;
}
.detail-badge {
    background: #EFF6FF;
    padding: 8px 15px;
    border-radius: 25px;
    color: #1E3A8A;
    font-size: 14px;
}
.detail-badge strong {
    color: #D4AF37;
}
.highlight-box {
    background: linear-gradient(135deg, #EFF6FF, #FFFFFF);
    border-left: 4px solid #D4AF37;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
.country-section {
    margin: 30px 0;
}
.country-title {
    font-size: 28px;
    color: #1E3A8A;
    margin-bottom: 20px;
    padding-left: 15px;
    border-left: 5px solid #D4AF37;
}
.comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.comparison-table th {
    background: #1E3A8A;
    color: white;
    padding: 15px;
    text-align: left;
}
.comparison-table td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
}
.comparison-table tr:hover {
    background: #EFF6FF;
}
.timeline {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
    margin: 30px 0;
}
.timeline-step {
    flex: 1;
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    position: relative;
}
.timeline-number {
    background: #D4AF37;
    color: #1E3A8A;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin: 0 auto 15px;
}
.tip-box {
    background: #EFF6FF;
    border: 2px dashed #D4AF37;
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
}
</style>

<div class="scholarship-header">
    <h1 style="color: white; font-size: 36px;">🏆 Complete Guide to Scholarships in Asia</h1>
    <p style="font-size: 18px;">Your Gateway to Fully Funded Education in China, Singapore, Malaysia, Japan & Korea</p>
</div>

<div class="scholarship-stats">
    <div class="stat-card">
        <div class="stat-number">100%</div>
        <div>Tuition Coverage</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">¥3,500</div>
        <div>Monthly Stipend (CSC)</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">280+</div>
        <div>Universities</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">50,000+</div>
        <div>Scholarship Recipients</div>
    </div>
</div>

<h2>📚 Table of Contents</h2>
<ul>
    <li>1. Overview: Types of Scholarships in Asia</li>
    <li>2. 🇨🇳 Chinese Government Scholarship (CSC) – Complete Guide</li>
    <li>3. 🇸🇬 Singapore International Graduate Award (SINGA)</li>
    <li>4. 🇯🇵 Japanese Government (MEXT) Scholarship</li>
    <li>5. 🇰🇷 Korean Government Scholarship Program (KGSP)</li>
    <li>6. 🇲🇾 Malaysia International Scholarship (MIS)</li>
    <li>7. University-Specific Scholarships</li>
    <li>8. Application Timeline & Checklist</li>
    <li>9. Tips for Winning Scholarships</li>
    <li>10. Frequently Asked Questions</li>
</ul>

<h2 class="country-title">1. Overview: Types of Scholarships in Asia</h2>

<div class="highlight-box">
<p>Asian governments and universities offer some of the world's most generous scholarships, covering full tuition, living expenses, and even travel costs. Here's your complete guide to securing funding for your study abroad journey.</p>
</div>

<table class="comparison-table">
<thead>
<th>Scholarship</th>
<th>Country</th>
<th>Coverage</th>
<th>Deadline</th>
<th>Level</th>
</thead>
<tbody>
<tr><td>CSC Scholarship</td><td>🇨🇳 China</td><td>Full tuition + ¥2,500-3,500/month</td><td>Jan-Mar</td><td>Bachelor/Master/PhD</td></tr>
<tr><td>SINGA</td><td>🇸🇬 Singapore</td><td>Full tuition + SGD 2,200/month</td><td>Jun/Dec</td><td>PhD</td></tr>
<tr><td>MEXT</td><td>🇯🇵 Japan</td><td>Full tuition + ¥143,000/month</td><td>Apr-May</td><td>Bachelor/Master/PhD</td></tr>
<tr><td>KGSP</td><td>🇰🇷 Korea</td><td>Full tuition + KRW 900,000/month</td><td>Feb-Mar</td><td>Bachelor/Master/PhD</td></tr>
<tr><td>MIS</td><td>🇲🇾 Malaysia</td><td>Full tuition + RM 1,500/month</td><td>May</td><td>Master/PhD</td></tr>
</tbody>
</table>

<h2 class="country-title">2. 🇨🇳 Chinese Government Scholarship (CSC) – Complete Guide</h2>

<div class="scholarship-card">
    <div class="scholarship-title">Chinese Government Scholarship (CSC)</div>
    <p>The most prestigious scholarship in China, funded by the Chinese Ministry of Education. Over 280 universities participate, covering 100% of tuition and providing generous living stipends.</p>
    
    <div class="scholarship-details">
        <div class="detail-badge"><strong>💰 Coverage:</strong> Full tuition + accommodation + monthly stipend</div>
        <div class="detail-badge"><strong>💵 Stipend:</strong> Undergraduate ¥2,500 | Master ¥3,000 | PhD ¥3,500</div>
        <div class="detail-badge"><strong>📅 Duration:</strong> 4-5 years (Bachelor), 2-3 years (Master), 3-4 years (PhD)</div>
        <div class="detail-badge"><strong>🏛️ Universities:</strong> 280+ (Tsinghua, Peking, Fudan, etc.)</div>
    </div>
</div>

<h3>📋 Types of CSC Scholarships</h3>

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
    <div style="background: #EFF6FF; padding: 20px; border-radius: 15px;">
        <h4 style="color: #1E3A8A;">Type A – Bilateral Program</h4>
        <p>Apply through Chinese embassy in your home country. Each country has specific quotas (1-20 students). Deadline: January-March.</p>
    </div>
    <div style="background: #EFF6FF; padding: 20px; border-radius: 15px;">
        <h4 style="color: #1E3A8A;">Type B – Chinese University Program</h4>
        <p>Apply directly to universities. More flexible, 280+ participating universities. Deadline: February-April.</p>
    </div>
</div>

<h3>📝 Required Documents</h3>
<ul>
    <li>CSC Application Form (online)</li>
    <li>University Application Form</li>
    <li>Highest diploma (notarized copy)</li>
    <li>Academic transcripts (notarized)</li>
    <li>Study plan or research proposal (800-1,500 words)</li>
    <li>Two recommendation letters from professors</li>
    <li>Passport copy</li>
    <li>Physical examination form</li>
    <li>HSK/IELTS/TOEFL certificates</li>
</ul>

<h3>⏰ Application Timeline</h3>
<div class="timeline">
    <div class="timeline-step">
        <div class="timeline-number">1</div>
        <strong>Jan-Feb</strong>
        <p>Prepare documents</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">2</div>
        <strong>Mar-Apr</strong>
        <p>Submit applications</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">3</div>
        <strong>May-Jun</strong>
        <p>University review</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">4</div>
        <strong>Jul-Aug</strong>
        <p>Results announced</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">5</div>
        <strong>Sep</strong>
        <p>Begin studies</p>
    </div>
</div>

<h2 class="country-title">3. 🇸🇬 Singapore International Graduate Award (SINGA)</h2>

<div class="scholarship-card">
    <div class="scholarship-title">Singapore International Graduate Award (SINGA)</div>
    <p>Prestigious PhD scholarship jointly offered by NTU, NUS, SUTD, SIT, and SMU. Designed for outstanding international graduates pursuing PhD studies in STEM fields.</p>
    
    <div class="scholarship-details">
        <div class="detail-badge"><strong>💰 Coverage:</strong> Full tuition + SGD 2,200/month stipend</div>
        <div class="detail-badge"><strong>✈️ Airfare:</strong> SGD 1,500 one-time</div>
        <div class="detail-badge"><strong>🏠 Settling-in:</strong> SGD 1,000 allowance</div>
        <div class="detail-badge"><strong>📅 Duration:</strong> Up to 4 years</div>
    </div>
</div>

<h3>🎯 Research Areas</h3>
<ul>
    <li>Biomedical Sciences</li>
    <li>Computing & Information Sciences</li>
    <li>Engineering & Technology</li>
    <li>Physical Sciences</li>
    <li>Materials Science</li>
</ul>

<h3>📅 Important Deadlines</h3>
<ul>
    <li><strong>June Intake:</strong> Apply by December 1</li>
    <li><strong>January Intake:</strong> Apply by June 1</li>
</ul>

<h2 class="country-title">4. 🇯🇵 Japanese Government (MEXT) Scholarship</h2>

<div class="scholarship-card">
    <div class="scholarship-title">Japanese Government (MEXT) Scholarship</div>
    <p>The most prestigious scholarship in Japan, offered by the Ministry of Education, Culture, Sports, Science and Technology.</p>
    
    <div class="scholarship-details">
        <div class="detail-badge"><strong>💰 Stipend:</strong> ¥143,000-148,000/month</div>
        <div class="detail-badge"><strong>✈️ Airfare:</strong> Round-trip economy class</div>
        <div class="detail-badge"><strong>📚 Tuition:</strong> Full waiver</div>
        <div class="detail-badge"><strong>🏥 Insurance:</strong> Comprehensive coverage</div>
    </div>
</div>

<h3>📋 Types of MEXT Scholarships</h3>
<ul>
    <li><strong>Research Student:</strong> 1.5-2 years (Master's/PhD)</li>
    <li><strong>Undergraduate:</strong> 5 years (including 1 year language)</li>
    <li><strong>Teacher Training:</strong> 1.5 years</li>
    <li><strong>Japanese Studies:</strong> 1 year</li>
</ul>

<h2 class="country-title">5. 🇰🇷 Korean Government Scholarship Program (KGSP)</h2>

<div class="scholarship-card">
    <div class="scholarship-title">Korean Government Scholarship Program (KGSP)</div>
    <p>Funded by the Korean Ministry of Education, bringing international students to top Korean universities.</p>
    
    <div class="scholarship-details">
        <div class="detail-badge"><strong>💰 Stipend:</strong> KRW 900,000-1,000,000/month</div>
        <div class="detail-badge"><strong>✈️ Airfare:</strong> Round-trip economy</div>
        <div class="detail-badge"><strong>📚 Korean Training:</strong> 1 year</div>
        <div class="detail-badge"><strong>🏛️ Universities:</strong> 65+ participating</div>
    </div>
</div>

<h3>🎯 Two Application Tracks</h3>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 20px 0;">
    <div style="background: #EFF6FF; padding: 20px; border-radius: 15px;">
        <h4 style="color: #1E3A8A;">Track A: Embassy Track</h4>
        <p>Apply through Korean embassy in your country. 1-5 students per country. Deadline: February-March.</p>
    </div>
    <div style="background: #EFF6FF; padding: 20px; border-radius: 15px;">
        <h4 style="color: #1E3A8A;">Track B: University Track</h4>
        <p>Apply directly to Korean universities. More spots available. Deadline: March-April.</p>
    </div>
</div>

<h2 class="country-title">6. 🇲🇾 Malaysia International Scholarship (MIS)</h2>

<div class="scholarship-card">
    <div class="scholarship-title">Malaysia International Scholarship (MIS)</div>
    <p>Funded by the Malaysian government for outstanding international students pursuing Master's and PhD programs.</p>
    
    <div class="scholarship-details">
        <div class="detail-badge"><strong>💰 Stipend:</strong> RM 1,500/month</div>
        <div class="detail-badge"><strong>📚 Tuition:</strong> Full waiver</div>
        <div class="detail-badge"><strong>✈️ Airfare:</strong> Round-trip economy</div>
        <div class="detail-badge"><strong>📅 Duration:</strong> 24-36 months</div>
    </div>
</div>

<h2 class="country-title">7. University-Specific Scholarships</h2>

<h3 style="color: #1E3A8A;">🇨🇳 China</h3>
<ul>
    <li><strong>Tsinghua University Scholarship:</strong> 50-100% tuition reduction</li>
    <li><strong>Peking University Scholarship:</strong> Full tuition + stipend</li>
    <li><strong>Fudan University Scholarship:</strong> 50-100% tuition + living allowance</li>
    <li><strong>Shanghai Jiao Tong University Scholarship:</strong> Full tuition + accommodation</li>
</ul>

<h3 style="color: #1E3A8A;">🇸🇬 Singapore</h3>
<ul>
    <li><strong>NUS Merit Scholarship:</strong> Full tuition + SGD 5,800/year</li>
    <li><strong>NTU Nanyang Scholarship:</strong> Full tuition + SGD 5,000/year</li>
    <li><strong>SMU Global Impact Scholarship:</strong> Full tuition + living allowance</li>
</ul>

<h3 style="color: #1E3A8A;">🇯🇵 Japan</h3>
<ul>
    <li><strong>University of Tokyo Scholarship:</strong> ¥150,000/month</li>
    <li><strong>Kyoto University Fellowship:</strong> ¥150,000/month</li>
    <li><strong>Waseda University Scholarship:</strong> Partial to full tuition</li>
</ul>

<h2 class="country-title">8. Application Timeline & Checklist</h2>

<div class="tip-box">
    <h3 style="color: #1E3A8A;">📅 18-Month Preparation Timeline</h3>
    <ul>
        <li><strong>18 Months Before:</strong> Research universities and scholarships</li>
        <li><strong>15 Months Before:</strong> Take language tests (IELTS/TOEFL/HSK/TOPIK/JLPT)</li>
        <li><strong>12 Months Before:</strong> Request recommendation letters, write personal statement</li>
        <li><strong>9 Months Before:</strong> Contact potential supervisors (for graduate programs)</li>
        <li><strong>6 Months Before:</strong> Submit applications</li>
        <li><strong>3 Months Before:</strong> Prepare visa documents</li>
    </ul>
</div>

<h3>📋 Essential Documents Checklist</h3>
<div class="highlight-box">
<ul>
    <li>☐ Valid passport (6+ months validity)</li>
    <li>☐ Academic transcripts (notarized)</li>
    <li>☐ Degree certificates (notarized)</li>
    <li>☐ Language test scores (IELTS/TOEFL/HSK/TOPIK/JLPT)</li>
    <li>☐ Personal statement (1,000-2,000 words)</li>
    <li>☐ Research proposal (2,000+ words for graduate)</li>
    <li>☐ 2-3 recommendation letters from professors</li>
    <li>☐ Curriculum Vitae (CV) with publications</li>
    <li>☐ Physical examination form</li>
    <li>☐ Portfolio (for arts/design programs)</li>
</ul>
</div>

<h2 class="country-title">9. Tips for Winning Scholarships</h2>

<div class="scholarship-card">
    <h3 style="color: #1E3A8A;">🎯 Expert Advice from Scholarship Winners</h3>
    
    <h4>1. Start Early</h4>
    <p>Begin your scholarship search 12-18 months before your intended start date. Top scholarships have strict deadlines and require extensive preparation.</p>
    
    <h4>2. Research Your Target</h4>
    <p>Understand what each scholarship values. CSC looks for academic excellence and research potential. KGSP values leadership and cultural exchange. Tailor your application accordingly.</p>
    
    <h4>3. Write a Compelling Personal Statement</h4>
    <p>Your personal statement should tell YOUR story. Why do you want to study in this country? What makes you unique? How will you contribute?</p>
    
    <h4>4. Get Strong Recommendation Letters</h4>
    <p>Ask professors who know you well. Provide them with your CV, transcripts, and personal statement so they can write specific, detailed letters.</p>
    
    <h4>5. Prepare for Interviews</h4>
    <p>Many scholarships require interviews. Practice answering questions about your academic background, research interests, and future goals. Be authentic and passionate.</p>
    
    <h4>6. Apply to Multiple Scholarships</h4>
    <p>Don't put all your eggs in one basket. Apply to 3-5 scholarships to increase your chances.</p>
</div>

<h2 class="country-title">10. Frequently Asked Questions</h2>

<div class="scholarship-card">
    <h3>❓ Can I apply for multiple scholarships?</h3>
    <p>Yes! Apply to as many as you're eligible for. However, if you receive multiple awards, you usually need to choose one.</p>
    
    <h3>❓ Do I need to know the local language?</h3>
    <p>For English-taught programs, you need IELTS/TOEFL. For local language programs, you need HSK (China), TOPIK (Korea), or JLPT (Japan).</p>
    
    <h3>❓ What GPA do I need?</h3>
    <p>Most scholarships require 80%+ (3.0/4.0 GPA). Competitive ones require 85%+ (3.5/4.0 GPA).</p>
    
    <h3>❓ Can I work while on scholarship?</h3>
    <p>Yes, with restrictions. Most allow 20 hours/week during semesters and full-time during breaks.</p>
    
    <h3>❓ What if my application is rejected?</h3>
    <p>Don't give up! Many successful applicants apply multiple times. Get feedback, improve your application, and try again next cycle.</p>
</div>

<div class="tip-box" style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; text-align: center;">
    <h2 style="color: white;">🏆 Your Dream Education is Within Reach!</h2>
    <p style="font-size: 18px;">With determination, preparation, and the right guidance, you can secure a fully funded scholarship to Asia's top universities.</p>
    <p><strong>Start your application today! 🇨🇳🇸🇬🇯🇵🇰🇷🇲🇾</strong></p>
</div>
'''

# Update Article 2 (Scholarships)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 2", (scholarship_content,))
print("✅ Updated Scholarship Guide article (ID 2)")


# ==================== ARTICLE 3: COMPLETE VISA GUIDE - PREMIUM DESIGN ====================
visa_content = '''
<style>
.visa-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2D4FA8 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}
.visa-stats {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: linear-gradient(135deg, #D4AF37, #F3D03E);
    color: #1E3A8A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.country-tab {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 30px 0;
}
.tab-btn {
    background: white;
    border: 2px solid #1E3A8A;
    padding: 12px 25px;
    border-radius: 40px;
    color: #1E3A8A;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}
.tab-btn:hover, .tab-btn.active {
    background: #1E3A8A;
    color: white;
}
.visa-card {
    background: white;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-left: 5px solid #D4AF37;
    display: none;
}
.visa-card.active {
    display: block;
}
.visa-title {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}
.visa-title .flag {
    font-size: 48px;
}
.visa-title h2 {
    color: #1E3A8A;
    font-size: 32px;
    margin: 0;
}
.step-timeline {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 30px 0;
}
.step {
    flex: 1;
    background: #EFF6FF;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    position: relative;
}
.step-number {
    background: #D4AF37;
    color: #1E3A8A;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin: 0 auto 15px;
}
.document-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 20px 0;
}
.document-item {
    background: #EFF6FF;
    padding: 12px 15px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.document-item:before {
    content: "✓";
    color: #D4AF37;
    font-weight: bold;
    font-size: 18px;
}
.info-box {
    background: #EFF6FF;
    border-left: 4px solid #D4AF37;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
.warning-box {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
.timeline-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.timeline-table th {
    background: #1E3A8A;
    color: white;
    padding: 12px;
    text-align: left;
}
.timeline-table td {
    padding: 12px;
    border-bottom: 1px solid #e0e0e0;
}
</style>

<div class="visa-header">
    <h1 style="color: white; font-size: 36px;">🛂 Complete Student Visa Guide for Asia</h1>
    <p style="font-size: 18px;">Your Step-by-Step Guide to Getting a Student Visa for China, Singapore, Malaysia, Japan & Korea</p>
</div>

<div class="visa-stats">
    <div class="stat-card">
        <div class="stat-number">95%</div>
        <div>Approval Rate</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">2-4</div>
        <div>Weeks Processing</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">$50-200</div>
        <div>Visa Fee</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">30-90</div>
        <div>Days to Arrive</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div>Support Available</div>
    </div>
</div>

<div class="country-tab">
    <button class="tab-btn active" onclick="showVisa('china')">🇨🇳 China</button>
    <button class="tab-btn" onclick="showVisa('singapore')">🇸🇬 Singapore</button>
    <button class="tab-btn" onclick="showVisa('malaysia')">🇲🇾 Malaysia</button>
    <button class="tab-btn" onclick="showVisa('japan')">🇯🇵 Japan</button>
    <button class="tab-btn" onclick="showVisa('korea')">🇰🇷 Korea</button>
</div>

<!-- China Visa -->
<div id="china" class="visa-card active">
    <div class="visa-title">
        <span class="flag">🇨🇳</span>
        <h2>China Student Visa (X1 & X2)</h2>
    </div>
    
    <div class="step-timeline">
        <div class="step">
            <div class="step-number">1</div>
            <strong>Get Admission</strong>
            <p>Receive admission letter + JW201/JW202 form</p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <strong>Medical Exam</strong>
            <p>Complete Foreigner Physical Examination</p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <strong>Apply at Embassy</strong>
            <p>Submit documents, 4-7 working days</p>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <strong>Travel to China</strong>
            <p>Enter within 30 days of visa issuance</p>
        </div>
        <div class="step">
            <div class="step-number">5</div>
            <strong>Residence Permit</strong>
            <p>Apply at PSB within 30 days</p>
        </div>
    </div>
    
    <h3>📋 Required Documents</h3>
    <div class="document-list">
        <div class="document-item">Valid passport (6+ months validity)</div>
        <div class="document-item">Visa application form + photo</div>
        <div class="document-item">Admission letter from university</div>
        <div class="document-item">JW201/JW202 form</div>
        <div class="document-item">Physical examination record</div>
        <div class="document-item">Bank statements ($10,000+)</div>
        <div class="document-item">Academic transcripts</div>
        <div class="document-item">Language proficiency (HSK/IELTS)</div>
    </div>
    
    <div class="info-box">
        <h3>⏰ Processing Time & Fees</h3>
        <ul>
            <li><strong>Processing:</strong> 4-7 working days</li>
            <li><strong>Visa Fee:</strong> $140-200 (varies by country)</li>
            <li><strong>X1 Visa:</strong> For long-term study (>180 days)</li>
            <li><strong>X2 Visa:</strong> For short-term study (<180 days)</li>
        </ul>
    </div>
    
    <div class="warning-box">
        <h3>⚠️ Important Notes</h3>
        <ul>
            <li>Apply for Residence Permit within 30 days of arrival</li>
            <li>Register at local police station within 24 hours</li>
            <li>Keep your passport with you at all times</li>
            <li>Report address changes to PSB within 10 days</li>
        </ul>
    </div>
</div>

<!-- Singapore Visa -->
<div id="singapore" class="visa-card">
    <div class="visa-title">
        <span class="flag">🇸🇬</span>
        <h2>Singapore Student Pass</h2>
    </div>
    
    <div class="step-timeline">
        <div class="step">
            <div class="step-number">1</div>
            <strong>University Admission</strong>
            <p>Receive offer letter from Singapore university</p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <strong>SOLAR Registration</strong>
            <p>University registers you in SOLAR system</p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <strong>Apply Online</strong>
            <p>Submit Student's Pass application, 2-4 weeks</p>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <strong>Medical Check</strong>
            <p>Complete medical examination in Singapore</p>
        </div>
        <div class="step">
            <div class="step-number">5</div>
            <strong>Collect Student Pass</strong>
            <p>Complete formalities at ICA</p>
        </div>
    </div>
    
    <div class="document-list">
        <div class="document-item">Valid passport</div>
        <div class="document-item">SOLAR registration number</div>
        <div class="document-item">Admission letter</div>
        <div class="document-item">Financial proof (SGD 30,000+)</div>
        <div class="document-item">Medical report</div>
        <div class="document-item">Passport photos</div>
        <div class="document-item">Academic transcripts</div>
        <div class="document-item">Visa application fee: SGD 30-90</div>
    </div>
    
    <div class="info-box">
        <h3>⏰ Processing Time & Fees</h3>
        <ul>
            <li><strong>Processing:</strong> 2-4 weeks</li>
            <li><strong>Visa Fee:</strong> SGD 30-90</li>
            <li><strong>Student Pass Fee:</strong> SGD 90</li>
            <li><strong>Validity:</strong> Duration of your course</li>
        </ul>
    </div>
    
    <div class="warning-box">
        <h3>⚠️ Important Notes</h3>
        <ul>
            <li>Must hold Student Pass for duration of studies</li>
            <li>Work allowed up to 16 hours/week during semester</li>
            <li>Part-time work allowed full-time during vacations</li>
            <li>Renew Student Pass before expiry</li>
        </ul>
    </div>
</div>

<!-- Malaysia Visa -->
<div id="malaysia" class="visa-card">
    <div class="visa-title">
        <span class="flag">🇲🇾</span>
        <h2>Malaysia Student Visa</h2>
    </div>
    
    <div class="step-timeline">
        <div class="step">
            <div class="step-number">1</div>
            <strong>University Admission</strong>
            <p>Receive offer letter from university</p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <strong>VAL Application</strong>
            <p>University applies for VAL, 2-4 weeks</p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <strong>Apply SEV</strong>
            <p>Single Entry Visa at embassy, 3-7 days</p>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <strong>Travel to Malaysia</strong>
            <p>Enter with 30-day special pass</p>
        </div>
        <div class="step">
            <div class="step-number">5</div>
            <strong>Student Pass Endorsement</strong>
            <p>Complete at Immigration, 1-2 weeks</p>
        </div>
    </div>
    
    <div class="document-list">
        <div class="document-item">Valid passport (18+ months validity)</div>
        <div class="document-item">Visa Approval Letter (VAL)</div>
        <div class="document-item">Admission letter</div>
        <div class="document-item">Medical report</div>
        <div class="document-item">Insurance</div>
        <div class="document-item">Financial proof (RM 20,000+)</div>
        <div class="document-item">Passport photos (white background)</div>
        <div class="document-item">Academic transcripts</div>
    </div>
    
    <div class="info-box">
        <h3>⏰ Processing Time & Fees</h3>
        <ul>
            <li><strong>VAL:</strong> 2-4 weeks</li>
            <li><strong>SEV:</strong> 3-7 working days</li>
            <li><strong>Student Pass:</strong> 1-2 weeks</li>
            <li><strong>Visa Fee:</strong> RM 100-200 ($20-40)</li>
        </ul>
    </div>
</div>

<!-- Japan Visa -->
<div id="japan" class="visa-card">
    <div class="visa-title">
        <span class="flag">🇯🇵</span>
        <h2>Japan Student Visa</h2>
    </div>
    
    <div class="step-timeline">
        <div class="step">
            <div class="step-number">1</div>
            <strong>University Admission</strong>
            <p>Receive Certificate of Admission</p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <strong>COE Application</strong>
            <p>University applies for COE, 1-3 months</p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <strong>Visa Application</strong>
            <p>Submit COE to embassy, 5-10 days</p>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <strong>Travel to Japan</strong>
            <p>Receive Residence Card at airport</p>
        </div>
        <div class="step">
            <div class="step-number">5</div>
            <strong>Alien Registration</strong>
            <p>Register within 14 days</p>
        </div>
    </div>
    
    <div class="document-list">
        <div class="document-item">Valid passport</div>
        <div class="document-item">Certificate of Eligibility (COE)</div>
        <div class="document-item">Admission letter</div>
        <div class="document-item">Financial proof (¥1,500,000+)</div>
        <div class="document-item">Academic transcripts</div>
        <div class="document-item">Study plan</div>
        <div class="document-item">JLPT certificate (if applicable)</div>
        <div class="document-item">Visa application form</div>
    </div>
    
    <div class="info-box">
        <h3>⏰ Processing Time & Fees</h3>
        <ul>
            <li><strong>COE:</strong> 1-3 months</li>
            <li><strong>Visa:</strong> 5-10 working days</li>
            <li><strong>Visa Fee:</strong> ¥3,000-6,000 ($20-40)</li>
            <li><strong>Residence Card:</strong> Free</li>
        </ul>
    </div>
    
    <div class="warning-box">
        <h3>⚠️ Important Notes</h3>
        <ul>
            <li>Work allowed up to 28 hours/week with permission</li>
            <li>Apply for work permit at immigration</li>
            <li>Notify address changes within 14 days</li>
            <li>Renew visa before expiry</li>
        </ul>
    </div>
</div>

<!-- Korea Visa -->
<div id="korea" class="visa-card">
    <div class="visa-title">
        <span class="flag">🇰🇷</span>
        <h2>Korea Student Visa (D-2)</h2>
    </div>
    
    <div class="step-timeline">
        <div class="step">
            <div class="step-number">1</div>
            <strong>University Admission</strong>
            <p>Receive admission letter</p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <strong>Prepare Documents</strong>
            <p>Financial proof, transcripts, study plan</p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <strong>Visa Application</strong>
            <p>Apply at Korean embassy, 7-14 days</p>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <strong>Enter Korea</strong>
            <p>Receive Alien Registration Card</p>
        </div>
        <div class="step">
            <div class="step-number">5</div>
            <strong>Register at Immigration</strong>
            <p>Complete within 90 days</p>
        </div>
    </div>
    
    <div class="document-list">
        <div class="document-item">Valid passport</div>
        <div class="document-item">Visa application form</div>
        <div class="document-item">Certificate of Admission</div>
        <div class="document-item">Financial proof ($10,000+)</div>
        <div class="document-item">Academic transcripts</div>
        <div class="document-item">Study plan</div>
        <div class="document-item">TOPIK certificate (if applicable)</div>
        <div class="document-item">Passport photos</div>
    </div>
    
    <div class="info-box">
        <h3>📋 Types of D-2 Visas</h3>
        <ul>
            <li><strong>D-2-1:</strong> Associate degree programs</li>
            <li><strong>D-2-2:</strong> Bachelor's degree programs</li>
            <li><strong>D-2-3:</strong> Master's degree programs</li>
            <li><strong>D-2-4:</strong> Doctoral degree programs</li>
            <li><strong>D-2-6:</strong> Exchange programs</li>
        </ul>
    </div>
    
    <div class="warning-box">
        <h3>⚠️ Important Notes</h3>
        <ul>
            <li>Work allowed up to 20 hours/week after 6 months</li>
            <li>Apply for Alien Registration Card within 90 days</li>
            <li>Part-time work permit required</li>
            <li>Report address changes to immigration</li>
        </ul>
    </div>
</div>

<h2>📊 Visa Processing Comparison</h2>
<table class="timeline-table">
    <thead>
        <th>Country</th>
        <th>Visa Type</th>
        <th>Processing Time</th>
        <th>Fee (USD)</th>
        <th>Work Allowed</th>
    </thead>
    <tbody>
        <tr><td>🇨🇳 China</td><td>X1/X2</td><td>4-7 days</td><td>$140-200</td><td>Yes (20 hrs/week)</td></tr>
        <tr><td>🇸🇬 Singapore</td><td>Student Pass</td><td>2-4 weeks</td><td>$20-70</td><td>Yes (16 hrs/week)</td></tr>
        <tr><td>🇲🇾 Malaysia</td><td>Student Pass</td><td>2-4 weeks</td><td>$20-40</td><td>Limited on-campus</td></tr>
        <tr><td>🇯🇵 Japan</td><td>Student Visa</td><td>1-3 months</td><td>$20-40</td><td>Yes (28 hrs/week)</td></tr>
        <tr><td>🇰🇷 Korea</td><td>D-2</td><td>7-14 days</td><td>$40-80</td><td>Yes (20 hrs/week)</td></tr>
    </tbody>
</table>

<div class="info-box">
    <h3>💡 Pro Tips for Visa Success</h3>
    <ul>
        <li><strong>Start Early:</strong> Begin visa process 3-4 months before departure</li>
        <li><strong>Double-Check Documents:</strong> Missing documents are the #1 reason for delays</li>
        <li><strong>Show Financial Stability:</strong> Prepare bank statements showing sufficient funds</li>
        <li><strong>Be Honest:</strong> Never falsify information on visa applications</li>
        <li><strong>Prepare for Interview:</strong> Know your study plan and why you chose that country</li>
    </ul>
</div>

<script>
function showVisa(country) {
    // Hide all visa cards
    document.querySelectorAll('.visa-card').forEach(card => {
        card.classList.remove('active');
    });
    // Show selected visa card
    document.getElementById(country).classList.add('active');
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}
</script>

<div style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); padding: 40px; border-radius: 20px; text-align: center; margin-top: 30px; color: white;">
    <h2 style="color: white;">🎓 Ready to Start Your Visa Application?</h2>
    <p style="font-size: 18px;">With proper preparation and documentation, your student visa journey can be smooth and successful!</p>
    <p><strong>Good luck on your study abroad adventure! 🌏</strong></p>
</div>
'''

# Update Article 3 (Visa Guide)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 3", (visa_content,))
print("✅ Updated Visa Guide article (ID 3)")


# ==================== ARTICLE 4: LEARNING MANDARIN - COMPLETE GUIDE ====================
mandarin_content = '''
<h1>🇨🇳 Complete Guide to Learning Mandarin: From Zero to Fluency</h1>

<div class="info-box">
<h3>📊 Quick Overview</h3>
<ul>
<li>📚 1.4 Billion Speakers | 2nd Most Spoken Language in World</li>
<li>✍️ 50,000+ Chinese Characters | 3,500 Commonly Used</li>
<li>🎓 HSK 6 Levels | Required for University Admission</li>
<li>⏱️ 2,200 Hours to Fluency (FSI Rating)</li>
<li>💰 Course Cost: ¥2,000-15,000/year ($280-2,100 USD)</li>
</ul>
</div>

<h2>📖 Table of Contents</h2>
<ul>
<li>1. Why Learn Mandarin?</li>
<li>2. Understanding Chinese Characters (Hanzi)</li>
<li>3. Pinyin: The Romanization System</li>
<li>4. The 4 Tones + Neutral Tone</li>
<li>5. HSK Exam Guide (Levels 1-6)</li>
<li>6. Best Apps and Resources</li>
<li>7. Study Plan: 0 to HSK 6</li>
<li>8. Mandarin Learning Tips from Successful Students</li>
<li>9. University Mandarin Programs</li>
<li>10. Language Exchange and Immersion</li>
<li>11. Common Mistakes to Avoid</li>
<li>12. Frequently Asked Questions</li>
</ul>

<h2>1. Why Learn Mandarin?</h2>
<p>Mandarin Chinese is the most spoken language in the world, with over 1.4 billion speakers. As China's global influence continues to grow, Mandarin proficiency has become an invaluable skill for international students, business professionals, and global citizens.</p>

<h3>1.1 Career Advantages</h3>
<p>Knowing Mandarin opens doors to careers in:</p>
<ul>
<li>International Business: China is the world's second-largest economy</li>
<li>Diplomacy and International Relations</li>
<li>Technology: China leads in AI, 5G, and e-commerce</li>
<li>Education and Translation</li>
<li>Tourism and Hospitality</li>
</ul>

<h3>1.2 Academic Requirements</h3>
<p>Most Chinese universities require HSK 4 for undergraduate programs and HSK 5 for graduate programs. Many CSC scholarships require at least HSK 4 for Chinese-taught programs.</p>

<h2>2. Understanding Chinese Characters (Hanzi)</h2>

<h3>2.1 History of Chinese Characters</h3>
<p>Chinese characters have evolved over 3,000 years from oracle bone script to modern simplified characters. Today, there are two writing systems:</p>
<ul>
<li><strong>Simplified Chinese:</strong> Used in mainland China, fewer strokes, easier to write</li>
<li><strong>Traditional Chinese:</strong> Used in Taiwan, Hong Kong, Macau, more strokes</li>
</ul>

<h3>2.2 Radicals: The Building Blocks</h3>
<p>Chinese characters are composed of radicals (radicals). There are 214 Kangxi radicals, but you only need to learn 100-150 common radicals to understand most characters.</p>

<h3>2.3 Stroke Order Rules</h3>
<p>Writing characters correctly requires proper stroke order:</p>
<ol>
<li>Top to bottom</li>
<li>Left to right</li>
<li>Horizontal before vertical</li>
<li>Outside before inside</li>
<li>Inside before outside (for enclosures)</li>
</ol>

<h3>2.4 Most Common Characters</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;">
<th>Character</th>
<th>Pinyin</th>
<th>Meaning</th>
<th>Radical</th>
<th>Frequency</th>
</tr>
</thead>
<tbody>
<tr><td>的</td><td>de</td><td>possessive particle</td><td>白 (white)</td><td>#1</td></tr>
<tr><td>一</td><td>yī</td><td>one</td><td>一 (one)</td><td>#2</td></tr>
<tr><td>了</td><td>le</td><td>completed action marker</td><td>了 (finish)</td><td>#3</td></tr>
<tr><td>是</td><td>shì</td><td>to be</td><td>日 (sun)</td><td>#4</td></tr>
<tr><td>不</td><td>bù</td><td>no, not</td><td>一 (one)</td><td>#5</td></tr>
<tr><td>我</td><td>wǒ</td><td>I, me</td><td>戈 (spear)</td><td>#6</td></tr>
<tr><td>在</td><td>zài</td><td>at, be located</td><td>土 (earth)</td><td>#7</td></tr>
<tr><td>人</td><td>rén</td><td>person</td><td>人 (person)</td><td>#8</td></tr>
<tr><td>有</td><td>yǒu</td><td>to have</td><td>月 (moon)</td><td>#9</td></tr>
<tr><td>这</td><td>zhè</td><td>this</td><td>辶 (walk)</td><td>#10</td></tr>
</tbody>
</table>

<h2>3. Pinyin: The Romanization System</h2>

<h3>3.1 What is Pinyin?</h3>
<p>Pinyin is the official romanization system for Standard Chinese, using the Latin alphabet to represent sounds. It's essential for learning pronunciation, typing on keyboards, and looking up characters in dictionaries.</p>

<h3>3.2 Initials (Consonants)</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;"><th>Initial</th><th>Pronunciation</th><th>Example</th></tr>
</thead>
<tbody>
<tr><td>b</td><td>like 'p' in 'spit'</td><td>bā (eight)</td></tr>
<tr><td>p</td><td>like 'p' in 'pit'</td><td>pá (climb)</td></tr>
<tr><td>m</td><td>like 'm' in 'mom'</td><td>mā (mother)</td></tr>
<tr><td>f</td><td>like 'f' in 'fan'</td><td>fā (hair)</td></tr>
<tr><td>d</td><td>like 't' in 'stop'</td><td>dà (big)</td></tr>
<tr><td>t</td><td>like 't' in 'top'</td><td>tā (he/she)</td></tr>
<tr><td>n</td><td>like 'n' in 'no'</td><td>nǐ (you)</td></tr>
<tr><td>l</td><td>like 'l' in 'love'</td><td>lè (happy)</td></tr>
<tr><td>g</td><td>like 'k' in 'skill'</td><td>gē (older brother)</td></tr>
<tr><td>k</td><td>like 'k' in 'kill'</td><td>kè (class)</td></tr>
</tbody>
</table>

<h3>3.3 Finals (Vowels)</h3>
<p>Finals can be simple vowels or compound finals. The main vowels are: a, o, e, i, u, ü.</p>

<h2>4. The 4 Tones + Neutral Tone</h2>
<p>Mandarin is a tonal language. The same syllable with different tones has different meanings. Mastering tones is crucial for being understood.</p>

<h3>4.1 The 4 Tones</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;"><th>Tone</th><th>Mark</th><th>Description</th><th>Example</th></tr>
</thead>
<tbody>
<tr><td>1st Tone</td><td>mā</td><td>High, flat (like singing a note)</td><td>妈 (mother)</td></tr>
<tr><td>2nd Tone</td><td>má</td><td>Rising (like asking a question)</td><td>麻 (hemp)</td></tr>
<tr><td>3rd Tone</td><td>mǎ</td><td>Falling then rising (dips)</td><td>马 (horse)</td></tr>
<tr><td>4th Tone</td><td>mà</td><td>Falling (like a command)</td><td>骂 (scold)</td></tr>
<tr><td>Neutral Tone</td><td>ma</td><td>Light, quick (no tone mark)</td><td>吗 (question particle)</td></tr>
</tbody>
</table>

<h2>5. HSK Exam Guide (Levels 1-6)</h2>

<h3>5.1 What is HSK?</h3>
<p>The Hanyu Shuiping Kaoshi (HSK) is the official Chinese proficiency test for non-native speakers. It's required for admission to Chinese universities, CSC scholarships, and employment in China.</p>

<h3>5.2 HSK Levels Overview</h3>
<table border="1" cellpadding="10" cellspacing="0" style="width:100%; border-collapse:collapse;">
<thead>
<tr style="background:#1E3A8A; color:white;">
<th>Level</th>
<th>Vocabulary</th>
<th>Characters</th>
<th>Study Hours</th>
<th>Can Do</th>
</tr>
</thead>
<tbody>
<tr><td><strong>HSK 1</strong></td><td>150 words</td><td>150 characters</td><td>150-250 hrs</td><td>Basic daily expressions</td></tr>
<tr><td><strong>HSK 2</strong></td><td>300 words</td><td>300 characters</td><td>300-400 hrs</td><td>Simple conversations</td></tr>
<tr><td><strong>HSK 3</strong></td><td>600 words</td><td>600 characters</td><td>450-600 hrs</td><td>Basic life and study</td></tr>
<tr><td><strong>HSK 4</strong></td><td>1,200 words</td><td>1,200 characters</td><td>600-800 hrs</td><td>Fluent conversation</td></tr>
<tr><td><strong>HSK 5</strong></td><td>2,500 words</td><td>2,500 characters</td><td>800-1,200 hrs</td><td>Reading newspapers</td></tr>
<tr><td><strong>HSK 6</strong></td><td>5,000+ words</td><td>5,000+ characters</td><td>1,200-2,200 hrs</td><td>Near-native fluency</td></tr>
</tbody>
</table>

<h3>5.3 HSK Requirements for Universities</h3>
<ul>
<li><strong>Undergraduate Programs:</strong> HSK 4 (180+) or HSK 5 (recommended)</li>
<li><strong>Graduate Programs:</strong> HSK 5 (180+) or HSK 6 (recommended)</li>
<li><strong>CSC Scholarship:</strong> HSK 4 minimum, HSK 5 for competitive universities</li>
<li><strong>Tsinghua/Peking:</strong> HSK 5 (200+) strongly recommended</li>
</ul>

<h3>5.4 HSK Exam Format</h3>
<ul>
<li><strong>Listening:</strong> 25-45 minutes</li>
<li><strong>Reading:</strong> 40-50 minutes</li>
<li><strong>Writing:</strong> 15-35 minutes (varies by level)</li>
<li><strong>Speaking:</strong> Optional HSKK test (Beginner, Intermediate, Advanced)</li>
</ul>

<h2>6. Best Apps and Resources</h2>

<h3>6.1 Free Apps</h3>
<ul>
<li><strong>Duolingo:</strong> Gamified learning, great for beginners</li>
<li><strong>HelloChinese:</strong> Specifically designed for Mandarin learners</li>
<li><strong>Pleco:</strong> The #1 Chinese dictionary app (essential!)</li>
<li><strong>Anki:</strong> Spaced repetition flashcards</li>
<li><strong>Skritter:</strong> Best for learning to write characters (free trial)</li>
<li><strong>ChineseSkill:</strong> Comprehensive learning app</li>
</ul>

<h3>6.2 Websites and Online Courses</h3>
<ul>
<li><strong>Coursera:</strong> Chinese for Beginners (Peking University)</li>
<li><strong>edX:</strong> Mandarin courses from Tsinghua, Shanghai Jiao Tong</li>
<li><strong>ChinesePod:</strong> Podcast-based learning, 4,000+ lessons</li>
<li><strong>Yoyo Chinese:</strong> Structured video courses</li>
<li><strong>HSK Online:</strong> Practice tests and vocabulary</li>
<li><strong>Purple Culture:</strong> Character writing resources</li>
</ul>

<h3>6.3 Books and Textbooks</h3>
<ul>
<li><strong>HSK Standard Course:</strong> Official HSK textbooks (Volumes 1-6)</li>
<li><strong>Integrated Chinese:</strong> Most widely used university textbook</li>
<li><strong>New Practical Chinese Reader:</strong> Classic textbook series</li>
<li><strong>Chinese Made Easier:</strong> Good for self-study</li>
<li><strong>Reading and Writing Chinese:</strong> Character guide</li>
</ul>

<h2>7. Study Plan: 0 to HSK 6</h2>

<h3>Week 1-4: Foundations</h3>
<ul>
<li>Master Pinyin pronunciation</li>
<li>Learn the 4 tones</li>
<li>Study 50 most common characters</li>
<li>Practice simple greetings and introductions</li>
</ul>

<h3>Months 1-3: HSK 1 (150 words)</h3>
<ul>
<li>30 minutes daily vocabulary study</li>
<li>10 new characters per day</li>
<li>Use flashcards daily</li>
<li>Practice speaking with language partner weekly</li>
</ul>

<h3>Months 4-6: HSK 2 (300 words)</h3>
<ul>
<li>Learn 10-15 new words daily</li>
<li>Start reading simple dialogues</li>
<li>Watch Chinese cartoons (Peppa Pig, Pleasant Goat)</li>
<li>HSK practice tests monthly</li>
</ul>

<h3>Months 7-12: HSK 3 (600 words)</h3>
<ul>
<li>Increase study to 1 hour daily</li>
<li>Start HSK 3 textbook</li>
<li>Watch Chinese dramas with subtitles</li>
<li>Write short essays daily</li>
</ul>

<h3>Year 2: HSK 4 (1,200 words)</h3>
<ul>
<li>2 hours daily study</li>
<li>Read Chinese news headlines</li>
<li>Listen to Chinese podcasts</li>
<li>Language exchange 2x weekly</li>
</ul>

<h3>Year 3-4: HSK 5-6 (2,500-5,000 words)</h3>
<ul>
<li>Immersion: consume Chinese media daily</li>
<li>Read Chinese novels and newspapers</li>
<li>Watch lectures and documentaries</li>
<li>Prepare for university admission</li>
</ul>

<h2>8. Mandarin Learning Tips from Successful Students</h2>

<h3>Tips from Students Who Passed HSK 6 in 2 Years</h3>
<div class="info-box">
<ul>
<li><strong>Daily consistency:</strong> 30 minutes every day beats 3 hours once a week</li>
<li><strong>Use it or lose it:</strong> Find speaking partners immediately</li>
<li><strong>Write characters daily:</strong> Muscle memory is key</li>
<li><strong>Watch with subtitles:</strong> Chinese audio, Chinese subtitles</li>
<li><strong>Sing karaoke:</strong> Great for tones and pronunciation</li>
<li><strong>Label everything:</strong> Put Chinese labels on household items</li>
<li><strong>Think in Chinese:</strong> Narrate your daily activities mentally</li>
<li><strong>Join language groups:</strong> WeChat groups, Discord servers</li>
</ul>
</div>

<h2>9. University Mandarin Programs</h2>

<h3>9.1 Top Language Programs in China</h3>
<ul>
<li><strong>Peking University (PKU):</strong> Intensive Chinese Language Program</li>
<li><strong>Beijing Language and Culture University (BLCU):</strong> #1 for Chinese language</li>
<li><strong>Fudan University:</strong> Chinese Language Program</li>
<li><strong>Shanghai Jiao Tong University:</strong> International Chinese Program</li>
<li><strong>Beijing Normal University:</strong> Chinese Language and Culture Program</li>
</ul>

<h3>9.2 Program Types</h3>
<ul>
<li><strong>Summer Program:</strong> 4-8 weeks, intensive immersion, HSK preparation</li>
<li><strong>Semester Program:</strong> 4-5 months, 15-20 hours/week</li>
<li><strong>Academic Year:</strong> 9-10 months, comprehensive language training</li>
<li><strong>Pre-University:</strong> 1-year foundation, pathway to degree programs</li>
</ul>

<h2>10. Language Exchange and Immersion</h2>

<h3>10.1 Finding Language Partners</h3>
<ul>
<li><strong>HelloTalk:</strong> Language exchange app, 20M+ users</li>
<li><strong>Tandem:</strong> Find native speakers for video calls</li>
<li><strong>Conversation Exchange:</strong> In-person meetings in your city</li>
<li><strong>WeChat:</strong> Join Chinese groups, follow Chinese media</li>
<li><strong>Meetup:</strong> Chinese language groups in your city</li>
</ul>

<h3>10.2 Immersion Strategies</h3>
<ul>
<li>Change phone language to Chinese</li>
<li>Listen to Chinese music daily (recommend: Jay Chou, JJ Lin)</li>
<li>Watch Chinese dramas (iQIYI, YouTube, Viki)</li>
<li>Read Chinese news (The Paper, Caixin, Sixth Tone)</li>
<li>Follow Chinese influencers on Weibo, Douyin</li>
<li>Order food in Chinese</li>
<li>Join Chinese clubs and events</li>
</ul>

<h2>11. Common Mistakes to Avoid</h2>

<h3>11.1 Pronunciation Mistakes</h3>
<ul>
<li>Ignoring tones completely</li>
<li>Mixing up 2nd and 3rd tones</li>
<li>Not distinguishing between j/q/x and zh/ch/sh</li>
<li>Saying 'r' like English 'r'</li>
</ul>

<h3>11.2 Grammar Mistakes</h3>
<ul>
<li>Overusing 是 (shì) for all "to be" situations</li>
<li>Wrong word order (Chinese is SVO)</li>
<li>Confusing 了 (le) usage</li>
<li>Using English grammar patterns</li>
</ul>

<h3>11.3 Character Mistakes</h3>
<ul>
<li>Ignoring radicals</li>
<li>Wrong stroke order</li>
<li>Relying too much on pinyin</li>
<li>Not learning to handwrite</li>
</ul>

<h2>12. Frequently Asked Questions</h2>

<h3>Q1: How long does it take to learn Mandarin?</h3>
<p>FSI estimates 2,200 hours for fluency. With 2 hours daily, about 3 years. HSK 4 can be achieved in 1.5-2 years.</p>

<h3>Q2: Is Mandarin the hardest language?</h3>
<p>It's challenging but not impossible. Writing takes time, but grammar is simpler than European languages (no tenses, no plurals, no gender).</p>

<h3>Q3: Do I need to learn to write characters?</h3>
<p>For HSK 4+, yes. For basic conversation, pinyin is fine. Most Chinese type on keyboards (pinyin input) but need to recognize characters.</p>

<h3>Q4: Can I learn Mandarin on my own?</h3>
<p>Yes, with apps, textbooks, and language partners. But classes or tutors help with pronunciation and structured learning.</p>

<h3>Q5: How important are tones?</h3>
<p>Very important! Wrong tones can completely change meaning. Example: mā (mother) vs mǎ (horse) vs mà (scold).</p>

<h3>Q6: What's the best way to learn characters?</h3>
<p>Learn radicals first, then use spaced repetition (Anki), practice stroke order, and write daily. Skritter is excellent for this.</p>

<h3>Q7: Which Chinese dialect should I learn?</h3>
<p>Standard Mandarin (Putonghua) is used in education, government, and media. It's the only language needed for university admission.</p>

<div class="info-box" style="background:#1E3A8A; color:white; text-align:center; padding:30px;">
<h2>📚 Start Your Mandarin Journey Today!</h2>
<p>Consistency is key. Practice daily, find a language partner, and immerse yourself in Chinese culture. Your journey to fluency starts now!</p>
<p><strong>🇨🇳 加油！(Jiāyóu!) Keep going! 🇨🇳</strong></p>
</div>
'''

# Update Article 4 (Learning Mandarin)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 4", (mandarin_content,))
print("✅ Updated Learning Mandarin article (ID 4)")

# ==================== ARTICLE 11: MALAYSIA - ULTRA DETAILED ====================
malaysia_content = '''
<h1>🇲🇾 Complete Guide to Studying in Malaysia: Universities, Costs, Scholarships & More</h1>

<div class="info-box">
<h3>📊 Quick Overview</h3>
<ul>
<li>🏛️ 20+ Public Universities | 50+ Private Universities</li>
<li>🌏 170,000+ International Students</li>
<li>💰 Tuition: RM 10,000-45,000/year ($2,100-9,600 USD)</li>
<li>🏠 Living Cost: RM 1,200-2,500/month ($250-550 USD)</li>
<li>📚 English Medium of Instruction</li>
<li>🎓 Degrees Recognized Worldwide</li>
</ul>
</div>

<h2>📖 Table of Contents</h2>
<ul>
<li>1. Why Study in Malaysia?</li>
<li>2. Top 30 Universities in Malaysia</li>
<li>3. Detailed University Profiles</li>
<li>4. Admission Requirements by Program</li>
<li>5. Tuition Fees by University</li>
<li>6. Scholarships & Financial Aid</li>
<li>7. Cost of Living Breakdown</li>
<li>8. Student Visa Process</li>
<li>9. Student Life & Culture</li>
<li>10. Career Opportunities After Graduation</li>
<li>11. Frequently Asked Questions</li>
</ul>

<h2>1. Why Study in Malaysia?</h2>
<p>Malaysia has emerged as one of Southeast Asia's premier education destinations, attracting students from over 100 countries. Here's why:</p>

<h3>1.1 World-Class Education</h3>
<p>Malaysian universities consistently rank among the world's best. The University of Malaya (UM) is ranked #65 globally, while several others rank in the top 200. Many universities have partnerships with prestigious institutions like the University of Cambridge, Harvard, and MIT.</p>

<h3>1.2 Affordable Tuition</h3>
<p>Compared to Western countries, Malaysia offers exceptional value. Tuition fees range from RM 10,000 to RM 45,000 per year ($2,100-9,600 USD), which is 60-80% cheaper than studying in the US, UK, or Australia.</p>

<h3>1.3 English-Medium Instruction</h3>
<p>All public and private universities in Malaysia use English as the primary language of instruction, making it accessible to international students from around the world.</p>

<h3>1.4 Multicultural Environment</h3>
<p>Malaysia's diverse population includes Malay, Chinese, Indian, and indigenous communities, creating a rich cultural tapestry. Students experience multiple cultures, festivals, and cuisines.</p>

<h3>1.5 Strategic Location</h3>
<p>Located in the heart of Southeast Asia, Malaysia is a gateway to exploring Thailand, Singapore, Indonesia, Vietnam, and beyond. Budget airlines offer flights for as low as RM 50 ($11).</p>

<h2>2. Top 30 Universities in Malaysia</h2>

<h3>Public Universities (20+ Universities)</h3>

<h4>2.1 University of Malaya (UM)</h4>
<p><strong>Ranking:</strong> #1 Malaysia, #65 World (QS 2026)</p>
<p><strong>Location:</strong> Kuala Lumpur</p>
<p><strong>Established:</strong> 1905</p>
<p><strong>Student Population:</strong> 30,000+ (18% international)</p>
<p><strong>Top Programs:</strong> Medicine (#51-100), Engineering (#101-150), Law (#101-150), Business (#101-150), Computer Science (#151-200)</p>
<p><strong>Tuition:</strong> RM 15,000-25,000/year</p>
<p><strong>Scholarships:</strong> UM Excellence Award (50-100% tuition), Malaysian Government Scholarship, ASEAN Scholarship</p>
<p><strong>Admission Requirements:</strong> High school diploma (85%+), IELTS 6.0/TOEFL 550, SAT 1200+ (recommended)</p>

<h4>2.2 Universiti Putra Malaysia (UPM)</h4>
<p><strong>Ranking:</strong> #2 Malaysia, #123 World</p>
<p><strong>Location:</strong> Serdang, Selangor</p>
<p><strong>Established:</strong> 1931</p>
<p><strong>Student Population:</strong> 28,000+ (15% international)</p>
<p><strong>Top Programs:</strong> Agriculture (#51-100), Veterinary Medicine (#51-100), Forestry (#101-150), Food Science (#101-150)</p>
<p><strong>Tuition:</strong> RM 14,000-24,000/year</p>

<h4>2.3 Universiti Kebangsaan Malaysia (UKM)</h4>
<p><strong>Ranking:</strong> #3 Malaysia, #141 World</p>
<p><strong>Location:</strong> Bangi, Selangor</p>
<p><strong>Established:</strong> 1970</p>
<p><strong>Top Programs:</strong> Medicine (#151-200), Pharmacy (#151-200), Law (#201-250), Islamic Studies (#51-100)</p>
<p><strong>Tuition:</strong> RM 14,000-23,000/year</p>

<h4>2.4 Universiti Sains Malaysia (USM)</h4>
<p><strong>Ranking:</strong> #4 Malaysia, #142 World</p>
<p><strong>Location:</strong> Penang</p>
<p><strong>Established:</strong> 1969</p>
<p><strong>Top Programs:</strong> Pharmacy (#101-150), Engineering (#201-250), Pure Sciences (#251-300)</p>
<p><strong>Tuition:</strong> RM 13,000-22,000/year</p>

<h4>2.5 Universiti Teknologi Malaysia (UTM)</h4>
<p><strong>Ranking:</strong> #5 Malaysia, #187 World</p>
<p><strong>Location:</strong> Johor Bahru</p>
<p><strong>Established:</strong> 1904</p>
<p><strong>Top Programs:</strong> Civil Engineering (#51-100), Mechanical Engineering (#101-150), Chemical Engineering (#101-150), Architecture (#101-150)</p>
<p><strong>Tuition:</strong> RM 14,000-24,000/year</p>

<h4>2.6 Universiti Utara Malaysia (UUM)</h4>
<p><strong>Ranking:</strong> #6 Malaysia, #551-600 World</p>
<p><strong>Location:</strong> Sintok, Kedah</p>
<p><strong>Specialization:</strong> Management, Business, Accounting, Economics</p>
<p><strong>Tuition:</strong> RM 9,000-15,000/year</p>

<h4>2.7 Universiti Malaysia Sabah (UMS)</h4>
<p><strong>Ranking:</strong> #7 Malaysia, #801-1000 World</p>
<p><strong>Location:</strong> Kota Kinabalu, Sabah</p>
<p><strong>Specialization:</strong> Marine Science, Tropical Biology, Tourism</p>
<p><strong>Tuition:</strong> RM 9,000-16,000/year</p>

<h4>2.8 Universiti Malaysia Sarawak (UNIMAS)</h4>
<p><strong>Ranking:</strong> #8 Malaysia, #801-1000 World</p>
<p><strong>Location:</strong> Kota Samarahan, Sarawak</p>
<p><strong>Specialization:</strong> Biodiversity, Conservation, Engineering</p>
<p><strong>Tuition:</strong> RM 9,000-17,000/year</p>

<h4>2.9 International Islamic University Malaysia (IIUM)</h4>
<p><strong>Ranking:</strong> #9 Malaysia, #601-650 World</p>
<p><strong>Location:</strong> Gombak, Selangor</p>
<p><strong>Specialization:</strong> Islamic Law, Economics, Engineering, Medicine</p>
<p><strong>Tuition:</strong> RM 12,000-22,000/year</p>

<h4>2.10 Universiti Malaysia Terengganu (UMT)</h4>
<p><strong>Ranking:</strong> #10 Malaysia, #801-1000 World</p>
<p><strong>Location:</strong> Terengganu</p>
<p><strong>Specialization:</strong> Marine Science, Fisheries, Oceanography</p>
<p><strong>Tuition:</strong> RM 8,000-14,000/year</p>

<h3>Private Universities (50+ Universities)</h3>

<h4>2.11 Taylor's University</h4>
<p><strong>Ranking:</strong> #1 Private University, #284 World</p>
<p><strong>Location:</strong> Subang Jaya, Selangor</p>
<p><strong>Top Programs:</strong> Hospitality & Tourism Management (#16 World), Business (#101-150), Medicine (#201-250), Pharmacy (#201-250)</p>
<p><strong>Tuition:</strong> RM 35,000-45,000/year</p>
<p><strong>International Students:</strong> 25% of total enrollment</p>

<h4>2.12 Sunway University</h4>
<p><strong>Ranking:</strong> #2 Private University, #601-650 World</p>
<p><strong>Location:</strong> Bandar Sunway, Selangor</p>
<p><strong>Partner:</strong> Lancaster University (UK)</p>
<p><strong>Top Programs:</strong> Business, Medicine, Psychology, Creative Arts, Computer Science</p>
<p><strong>Tuition:</strong> RM 30,000-40,000/year</p>

<h4>2.13 Multimedia University (MMU)</h4>
<p><strong>Ranking:</strong> #3 Private University, #701-750 World</p>
<p><strong>Location:</strong> Cyberjaya (Silicon Valley of Malaysia)</p>
<p><strong>Specialization:</strong> Computer Science, Software Engineering, Multimedia, Animation</p>
<p><strong>Tuition:</strong> RM 18,000-28,000/year</p>

<h4>2.14 Asia Pacific University (APU)</h4>
<p><strong>Ranking:</strong> #4 Private University, #801-1000 World</p>
<p><strong>Location:</strong> Kuala Lumpur</p>
<p><strong>Specialization:</strong> Computer Science, IT, Business, Engineering</p>
<p><strong>Tuition:</strong> RM 20,000-30,000/year</p>
<p><strong>International Students:</strong> 35% from 130+ countries</p>

<h4>2.15 UCSI University</h4>
<p><strong>Ranking:</strong> #5 Private University, #651-700 World</p>
<p><strong>Location:</strong> Cheras, Kuala Lumpur</p>
<p><strong>Specialization:</strong> Medicine, Pharmacy, Music, Engineering, Business</p>
<p><strong>Tuition:</strong> RM 25,000-45,000/year</p>

<h4>2.16 INTI International University</h4>
<p><strong>Ranking:</strong> #6 Private University</p>
<p><strong>Location:</strong> Nilai, Negeri Sembilan</p>
<p><strong>Partners:</strong> University of Hertfordshire (UK), Coventry University (UK)</p>
<p><strong>Tuition:</strong> RM 20,000-32,000/year</p>

<h4>2.17 SEGi University</h4>
<p><strong>Ranking:</strong> #7 Private University</p>
<p><strong>Location:</strong> Kota Damansara, Selangor</p>
<p><strong>Specialization:</strong> Medicine, Dentistry, Pharmacy, Engineering</p>
<p><strong>Tuition:</strong> RM 22,000-40,000/year</p>

<h4>2.18 Management & Science University (MSU)</h4>
<p><strong>Ranking:</strong> #8 Private University</p>
<p><strong>Location:</strong> Shah Alam, Selangor</p>
<p><strong>Specialization:</strong> Medicine, Pharmacy, Nursing, Business</p>
<p><strong>Tuition:</strong> RM 18,000-35,000/year</p>

<h4>2.19 Universiti Tunku Abdul Rahman (UTAR)</h4>
<p><strong>Ranking:</strong> #9 Private University, #601-650 World</p>
<p><strong>Location:</strong> Kampar, Perak & Sungai Long, Selangor</p>
<p><strong>Specialization:</strong> Engineering, Business, Chinese Studies, Medicine</p>
<p><strong>Tuition:</strong> RM 15,000-25,000/year (most affordable private)</p>

<h4>2.20 Infrastructure University Kuala Lumpur (IUKL)</h4>
<p><strong>Ranking:</strong> #10 Private University</p>
<p><strong>Location:</strong> Kajang, Selangor</p>
<p><strong>Specialization:</strong> Civil Engineering, Architecture, Quantity Surveying</p>
<p><strong>Tuition:</strong> RM 15,000-25,000/year</p>

<h2>3. Detailed University Profiles</h2>

<h3>3.1 University of Malaya (UM) - In-Depth</h3>
<p><strong>Faculties:</strong> 14 faculties offering 100+ programs</p>
<ul>
<li>Faculty of Medicine (est. 1962) - Malaysia's oldest medical school</li>
<li>Faculty of Engineering - Civil, Mechanical, Electrical, Chemical</li>
<li>Faculty of Law - Malaysia's premier law school</li>
<li>Faculty of Business & Economics - AACSB accredited</li>
<li>Faculty of Computer Science & IT - Strong AI and Data Science programs</li>
</ul>
<p><strong>Research Centers:</strong> 20+ research centers including the Institute of Advanced Studies, Centre for Nanotechnology, and Centre for Energy Sciences.</p>
<p><strong>Campus Facilities:</strong> 12 residential colleges, Olympic-size swimming pool, 10 libraries, 5 museums, and a teaching hospital.</p>
<p><strong>Notable Alumni:</strong> 5 Malaysian Prime Ministers, Nobel laureates, and leaders across Asia.</p>

<h3>3.2 Taylor's University - In-Depth</h3>
<p><strong>Schools:</strong> 8 schools offering 80+ programs</p>
<ul>
<li>School of Hospitality & Tourism (#16 World, #1 in Asia)</li>
<li>School of Medicine & Health Sciences</li>
<li>School of Engineering</li>
<li>School of Business</li>
<li>School of Architecture & Design</li>
<li>School of Computer Science</li>
<li>School of Pharmacy</li>
<li>School of Law</li>
</ul>
<p><strong>Campus:</strong> 27-acre campus with state-of-the-art facilities including the 5-star hospital and hospitality suite, engineering labs, and design studios.</p>
<p><strong>Industry Partnerships:</strong> Hilton, Marriott, Four Seasons, Google, Microsoft, and top law firms.</p>

<h2>4. Admission Requirements by Program</h2>

<h3>Undergraduate Programs</h3>
<table>
<thead><tr><th>Program Type</th><th>Academic Requirements</th><th>English Requirements</th></tr></thead>
<tbody>
<tr><td>Medicine</td><td>High school with Biology, Chemistry, Physics (85%+), A-Levels (AAA), STPM (4.0)</td><td>IELTS 6.5-7.0 or TOEFL 600+</td></tr>
<tr><td>Engineering</td><td>High school with Math, Physics, Chemistry (80%+), A-Levels (AAB), STPM (3.5+)</td><td>IELTS 6.0-6.5 or TOEFL 550+</td></tr>
<tr><td>Business</td><td>High school diploma (70%+), A-Levels (BBB), STPM (3.0+)</td><td>IELTS 5.5-6.0 or TOEFL 550+</td></tr>
<tr><td>Computer Science</td><td>High school with Math (75%+), A-Levels (BBB), STPM (3.0+)</td><td>IELTS 5.5-6.0</td></tr>
<tr><td>Law</td><td>High school diploma (75%+), A-Levels (AAB), STPM (3.5+)</td><td>IELTS 6.5-7.0</td></tr>
</tbody>
</table>

<h3>Graduate Programs (Master's & PhD)</h3>
<ul>
<li><strong>Master's by Coursework:</strong> Bachelor's degree with CGPA 2.75+, IELTS 6.0+</li>
<li><strong>Master's by Research:</strong> Bachelor's degree with CGPA 3.0+, research proposal, IELTS 6.0+</li>
<li><strong>PhD:</strong> Master's degree, strong research proposal, IELTS 6.5+, publications recommended</li>
</ul>

<h2>5. Tuition Fees by University (Annual)</h2>
<table>
<thead><tr><th>University</th><th>Undergraduate</th><th>Master's</th><th>PhD</th></tr></thead>
<tbody>
<tr><td>University of Malaya (UM)</td><td>RM 15,000-25,000</td><td>RM 18,000-30,000</td><td>RM 20,000-35,000</td></tr>
<tr><td>UPM</td><td>RM 14,000-24,000</td><td>RM 16,000-28,000</td><td>RM 18,000-30,000</td></tr>
<tr><td>UKM</td><td>RM 14,000-23,000</td><td>RM 16,000-26,000</td><td>RM 18,000-28,000</td></tr>
<tr><td>USM</td><td>RM 13,000-22,000</td><td>RM 15,000-25,000</td><td>RM 17,000-27,000</td></tr>
<tr><td>UTM</td><td>RM 14,000-24,000</td><td>RM 16,000-28,000</td><td>RM 18,000-30,000</td></tr>
<tr><td>Taylor's</td><td>RM 35,000-45,000</td><td>RM 38,000-50,000</td><td>RM 40,000-55,000</td></tr>
<tr><td>Sunway</td><td>RM 30,000-40,000</td><td>RM 35,000-45,000</td><td>RM 38,000-48,000</td></tr>
<tr><td>APU</td><td>RM 20,000-30,000</td><td>RM 22,000-35,000</td><td>RM 25,000-38,000</td></tr>
<tr><td>UCSI</td><td>RM 25,000-45,000</td><td>RM 28,000-48,000</td><td>RM 30,000-50,000</td></tr>
<tr><td>UTAR</td><td>RM 15,000-25,000</td><td>RM 18,000-28,000</td><td>RM 20,000-30,000</td></tr>
</tbody>
</table>

<h2>6. Scholarships & Financial Aid</h2>

<h3>Government Scholarships</h3>
<h4>Malaysia International Scholarship (MIS)</h4>
<p><strong>Coverage:</strong> Full tuition + monthly stipend RM 1,500 + accommodation + airfare</p>
<p><strong>Deadline:</strong> May 15 annually</p>
<p><strong>Eligibility:</strong> International students for Master's and PhD programs</p>
<p><strong>Application:</strong> Through Ministry of Higher Education Malaysia</p>

<h4>Commonwealth Scholarship</h4>
<p><strong>Coverage:</strong> Full tuition + living allowance + airfare</p>
<p><strong>Eligibility:</strong> Students from Commonwealth countries</p>
<p><strong>Deadline:</strong> March 31 annually</p>

<h4>MTCP Scholarship (Ministry of Education)</h4>
<p><strong>Coverage:</strong> Full tuition + monthly allowance RM 2,000 + airfare</p>
<p><strong>Eligibility:</strong> Students from developing countries</p>
<p><strong>Deadline:</strong> June 30 annually</p>

<h3>University Scholarships</h3>
<ul>
<li><strong>UM Excellence Award:</strong> 50-100% tuition waiver for top students</li>
<li><strong>UPM Graduate Research Scholarship:</strong> RM 2,500/month for PhD candidates</li>
<li><strong>UKM Chancellor's Scholarship:</strong> Full tuition for top 10% applicants</li>
<li><strong>USM Fellowship:</strong> Full tuition + RM 1,800/month stipend</li>
<li><strong>UTM International Student Scholarship:</strong> 50% tuition reduction</li>
<li><strong>Taylor's Excellence Award:</strong> 25-100% tuition for high achievers</li>
<li><strong>Sunway Merit Scholarship:</strong> 25-75% tuition based on academics</li>
<li><strong>APU International Scholarship:</strong> 10-50% tuition for international students</li>
</ul>

<h2>7. Cost of Living Breakdown</h2>

<h3>Accommodation Options</h3>
<table>
<thead><tr><th>Type</th><th>Monthly Cost (RM)</th><th>Description</th></tr></thead>
<tbody>
<tr><td>University Dormitory (single)</td><td>400-800</td><td>Shared facilities, close to campus</td></tr>
<tr><td>University Dormitory (twin)</td><td>250-500</td><td>2 sharing, basic amenities</td></tr>
<tr><td>Private Apartment (studio)</td><td>1,000-1,800</td><td>Fully furnished, city center</td></tr>
<tr><td>Private Apartment (2-bedroom)</td><td>1,500-2,500</td><td>Ideal for sharing with friends</td></tr>
<tr><td>Homestay</td><td>600-1,000</td><td>Live with Malaysian family</td></tr>
</tbody>
</table>

<h3>Food Expenses</h3>
<ul>
<li>University cafeteria: RM 3-8 per meal</li>
<li>Local restaurants (mamak): RM 5-10 per meal</li>
<li>Fast food: RM 10-15 per meal</li>
<li>Groceries (monthly): RM 200-300</li>
<li>Water/Ramadan bazaars: RM 5-10 per meal</li>
</ul>

<h3>Transportation</h3>
<ul>
<li>Public bus: RM 1-3 per trip</li>
<li>LRT/MRT: RM 2-5 per trip</li>
<li>Grab (ride-hailing): RM 8-20 per trip</li>
<li>Monthly public transport pass: RM 50-100</li>
<li>Student discount available on public transport</li>
</ul>

<h3>Monthly Budget Summary</h3>
<table>
<thead><tr><th>Category</th><th>Budget (RM)</th><th>Budget (USD)</th></tr></thead>
<tbody>
<tr><td>Accommodation</td><td>400-1,000</td><td>85-210</td></tr>
<tr><td>Food</td><td>600-900</td><td>130-190</td></tr>
<tr><td>Transport</td><td>100-150</td><td>20-30</td></tr>
<tr><td>Utilities & Internet</td><td>150-250</td><td>30-50</td></tr>
<tr><td>Mobile phone</td><td>30-50</td><td>6-10</td></tr>
<tr><td>Personal expenses</td><td>200-400</td><td>40-85</td></tr>
<tr><td><strong>Total</strong></td><td><strong>1,480-2,750</strong></td><td><strong>310-575</strong></td></tr>
</tbody>
</table>

<h2>8. Student Visa Process (Step-by-Step)</h2>

<h3>Step 1: Secure University Admission</h3>
<p>Receive offer letter from Education Malaysia Global Services (EMGS) registered university. Processing time: 2-4 weeks.</p>

<h3>Step 2: Apply for Visa Approval Letter (VAL)</h3>
<p>University submits application to EMGS. Required documents:</p>
<ul>
<li>Valid passport (min. 18 months validity)</li>
<li>Passport-sized photos (white background)</li>
<li>Academic transcripts & certificates</li>
<li>English proficiency proof (IELTS/TOEFL)</li>
<li>Health declaration form</li>
<li>Financial proof (RM 20,000+)</li>
</ul>
<p>Processing time: 2-4 weeks</p>

<h3>Step 3: Apply for Single Entry Visa (SEV)</h3>
<p>Take VAL and passport to nearest Malaysian embassy. Processing time: 3-7 working days. Cost: RM 100-200 ($20-40).</p>

<h3>Step 4: Arrive in Malaysia</h3>
<p>Upon arrival, you'll receive a 30-day special pass. Must complete Student Pass endorsement within 30 days.</p>

<h3>Step 5: Student Pass Endorsement</h3>
<p>Visit Malaysian Immigration Department with:</p>
<ul>
<li>Passport</li>
<li>Medical report</li>
<li>Insurance</li>
<li>University registration letter</li>
</ul>
<p>Processing time: 1-2 weeks. Student Pass valid for duration of studies.</p>

<h2>9. Student Life & Culture</h2>

<h3>Festivals & Holidays</h3>
<ul>
<li><strong>Hari Raya Aidilfitri:</strong> Celebration marking end of Ramadan (March/April)</li>
<li><strong>Chinese New Year:</strong> Lion dances, red envelopes (January/February)</li>
<li><strong>Deepavali:</strong> Festival of lights (October/November)</li>
<li><strong>Merdeka Day:</strong> Independence Day celebration (August 31)</li>
<li><strong>Malaysia Day:</strong> Formation of Malaysia (September 16)</li>
</ul>

<h3>Popular Student Cities</h3>
<ul>
<li><strong>Kuala Lumpur:</strong> Capital city, nightlife, shopping, food paradise</li>
<li><strong>Penang:</strong> UNESCO heritage site, beaches, street food, arts scene</li>
<li><strong>Johor Bahru:</strong> Close to Singapore, affordable living</li>
<li><strong>Ipoh:</strong> Heritage city, caves, delicious food</li>
<li><strong>Kota Kinabalu:</strong> Gateway to Mount Kinabalu, islands, diving</li>
<li><strong>Kuching:</strong> Nature, national parks, diverse culture</li>
</ul>

<h3>Student Activities</h3>
<ul>
<li>Clubs & Societies: Over 100 clubs per major university</li>
<li>Sports: Football, badminton, swimming, rugby, basketball</li>
<li>Cultural Exchange: Language exchange programs, cultural festivals</li>
<li>Outdoor Adventures: Hiking, camping, island trips</li>
<li>Volunteer Opportunities: Community service, environmental projects</li>
</ul>

<h2>10. Career Opportunities After Graduation</h2>

<h3>Job Placement Statistics</h3>
<ul>
<li>UM: 85% employed within 6 months of graduation</li>
<li>Taylor's: 90% employed, 70% in managerial positions</li>
<li>APU: 95% employed in tech sector</li>
<li>UTM: 88% employed in engineering fields</li>
</ul>

<h3>Top Employers in Malaysia</h3>
<ul>
<li><strong>Technology:</strong> Grab, Razer, Google Malaysia, Microsoft, Accenture</li>
<li><strong>Finance:</strong> Maybank, CIMB, Public Bank, Standard Chartered, HSBC</li>
<li><strong>Oil & Gas:</strong> Petronas, Shell, ExxonMobil, Schlumberger</li>
<li><strong>Manufacturing:</strong> Intel, Dell, HP, Bosch, Siemens</li>
<li><strong>Hospitality:</strong> Hilton, Marriott, Four Seasons, Shangri-La</li>
</ul>

<h3>Average Starting Salaries (Annual)</h3>
<table>
<thead><tr><th>Field</th><th>Annual Salary (RM)</th><th>Annual Salary (USD)</th></tr></thead>
<tbody>
<tr><td>Medicine</td><td>60,000-90,000</td><td>12,600-18,900</td></tr>
<tr><td>Engineering</td><td>40,000-60,000</td><td>8,400-12,600</td></tr>
<tr><td>Computer Science/IT</td><td>48,000-72,000</td><td>10,000-15,100</td></tr>
<tr><td>Business/Finance</td><td>36,000-54,000</td><td>7,600-11,300</td></tr>
<tr><td>Hospitality</td><td>30,000-45,000</td><td>6,300-9,500</td></tr>
</tbody>
</table>

<h2>11. Frequently Asked Questions (FAQ)</h2>

<h3>Q1: Is it safe to study in Malaysia?</h3>
<p>Yes, Malaysia is one of the safest countries in Southeast Asia. Universities have 24/7 security, and Malaysia ranks 18th in the Global Peace Index.</p>

<h3>Q2: Can I work while studying?</h3>
<p>Yes, international students can work part-time (up to 20 hours/week) during semester breaks. Common jobs include retail, F&B, and tutoring.</p>

<h3>Q3: Do I need to learn Malay?</h3>
<p>No, English is the medium of instruction. However, learning basic Malay phrases (Bahasa Malaysia) will enhance your experience.</p>

<h3>Q4: Can my family visit me?</h3>
<p>Yes, family members can apply for a Social Visit Pass (up to 30 days) or Long-Term Social Visit Pass for spouse/parents.</p>

<h3>Q5: What's the weather like?</h3>
<p>Tropical climate year-round: 25-35°C. Rainy season: November-March. Pack light clothing and an umbrella.</p>

<h3>Q6: Are there halal food options?</h3>
<p>Yes, Malaysia is a Muslim-majority country with abundant halal food options at all universities and restaurants.</p>

<h3>Q7: Can I stay after graduation?</h3>
<p>Yes, graduates can apply for the Employment Pass or Professional Visit Pass to work in Malaysia.</p>

<h3>Q8: What's the best time to apply?</h3>
<p>Main intake: September/October (apply by May-June). Secondary intake: February/March (apply by October-November).</p>

<div class="info-box">
<h3>🎓 Final Tips for Success</h3>
<ul>
<li>Start your application 6-8 months before the intake deadline</li>
<li>Research universities thoroughly - check rankings, accreditation, and alumni</li>
<li>Apply for multiple scholarships to increase chances</li>
<li>Connect with current students on LinkedIn for insights</li>
<li>Learn about Malaysian culture before arrival</li>
<li>Budget carefully and keep emergency funds</li>
<li>Build a network during your studies - it's invaluable for your career</li>
</ul>
</div>

<p><strong>With its world-class education, affordable costs, and vibrant culture, Malaysia offers an exceptional study abroad experience. Start your journey today!</strong> 🇲🇾</p>
'''

c.execute("UPDATE blog_posts SET content = ? WHERE id = 11", (malaysia_content,))
print("✅ Updated Malaysia article (ID 11)")

# ==================== ARTICLE 14 & 15: SINGAPORE COMPLETE GUIDE ====================
singapore_guide_content = '''
<style>
.sg-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2D4FA8 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}
.sg-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: linear-gradient(135deg, #D4AF37, #F3D03E);
    color: #1E3A8A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.university-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #D4AF37;
    transition: transform 0.3s;
}
.university-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(30,58,138,0.15);
}
.comparison-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.comparison-table th {
    background: #1E3A8A;
    color: white;
    padding: 12px;
    text-align: left;
}
.comparison-table td {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}
.scholarship-card {
    background: #EFF6FF;
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    border-left: 4px solid #D4AF37;
}
.timeline {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
    margin: 30px 0;
}
.timeline-step {
    flex: 1;
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}
.timeline-number {
    background: #D4AF37;
    color: #1E3A8A;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin: 0 auto 15px;
}
.tip-box {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
.cost-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.cost-table th {
    background: #1E3A8A;
    color: white;
    padding: 12px;
    text-align: left;
}
.cost-table td {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}
</style>

<div class="sg-header">
    <h1 style="color: white; font-size: 36px;">🇸🇬 Complete Guide to Studying in Singapore</h1>
    <p style="font-size: 18px;">Your Gateway to World-Class Education in Asia's Education Hub</p>
</div>

<div class="sg-stats">
    <div class="stat-card">
        <div class="stat-number">#8</div>
        <div>NUS World Ranking</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">#12</div>
        <div>NTU World Ranking</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">100,000+</div>
        <div>International Students</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">$1,500-3,000</div>
        <div>Monthly Living Cost</div>
    </div>
</div>

<h2>📖 Table of Contents</h2>
<ul>
    <li>1. Why Study in Singapore?</li>
    <li>2. Top Universities in Singapore</li>
    <li>3. Detailed University Profiles (NUS, NTU, SMU, SUTD, SIT)</li>
    <li>4. Admission Requirements</li>
    <li>5. Tuition Fees by University</li>
    <li>6. Scholarships Guide (SINGA, ASEAN, University Scholarships)</li>
    <li>7. Cost of Living Breakdown</li>
    <li>8. Student Visa Process (Student's Pass)</li>
    <li>9. Student Life & Culture</li>
    <li>10. Career Opportunities After Graduation</li>
    <li>11. Frequently Asked Questions</li>
</ul>

<h2>1. Why Study in Singapore?</h2>
<p>Singapore is consistently ranked as Asia's #1 education hub, with two universities in the world's top 20. The city-state offers world-class education, cutting-edge research facilities, and unparalleled career opportunities in a safe, multicultural environment.</p>

<h3>1.1 Academic Excellence</h3>
<p>Singapore's universities rank among the world's best: National University of Singapore (#8), Nanyang Technological University (#12), and Singapore Management University (#87). Research output is among the highest per capita globally.</p>

<h3>1.2 Strategic Location</h3>
<p>As Asia's financial and technology hub, Singapore is home to over 7,000 multinational corporations. Students have access to internships at Google, Facebook, Goldman Sachs, and local tech giants like Grab and Sea.</p>

<h3>1.3 Safe and Clean Environment</h3>
<p>Singapore is one of the safest countries in the world (ranked #1 for personal safety). The city is impeccably clean with excellent public infrastructure and world-class healthcare.</p>

<h3>1.4 Multicultural Society</h3>
<p>With 30% international students and a diverse population of Chinese, Malay, Indian, and expat communities, Singapore offers a truly global experience.</p>

<h2>2. Top Universities in Singapore</h2>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ 2.1 National University of Singapore (NUS)</h3>
    <p><strong>Ranking:</strong> #1 Singapore, #8 World, #1 Asia</p>
    <p><strong>Location:</strong> Kent Ridge, Singapore</p>
    <p><strong>Established:</strong> 1905</p>
    <p><strong>Student Population:</strong> 38,000+ (30% international)</p>
    <p><strong>Top Programs:</strong></p>
    <ul>
        <li>Computer Science: #4 World</li>
        <li>Engineering: #9 World</li>
        <li>Business: #15 World</li>
        <li>Law: #11 World</li>
        <li>Medicine: #20 World</li>
    </ul>
    <p><strong>Tuition:</strong> SGD 30,000-40,000/year ($22,000-30,000 USD)</p>
    <p><strong>Acceptance Rate:</strong> 10-15%</p>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ 2.2 Nanyang Technological University (NTU)</h3>
    <p><strong>Ranking:</strong> #2 Singapore, #12 World</p>
    <p><strong>Location:</strong> Yunnan Garden, Singapore</p>
    <p><strong>Established:</strong> 1991</p>
    <p><strong>Student Population:</strong> 33,000+ (28% international)</p>
    <p><strong>Top Programs:</strong></p>
    <ul>
        <li>Materials Science: #1 World</li>
        <li>Engineering: #4 World</li>
        <li>Computer Science: #15 World</li>
        <li>Business: #25 World</li>
    </ul>
    <p><strong>Tuition:</strong> SGD 28,000-38,000/year ($21,000-28,500 USD)</p>
    <p><strong>Note:</strong> "Greenest campus" in Asia</p>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ 2.3 Singapore Management University (SMU)</h3>
    <p><strong>Ranking:</strong> #3 Singapore, #87 World</p>
    <p><strong>Location:</strong> City Center, Singapore</p>
    <p><strong>Established:</strong> 2000</p>
    <p><strong>Student Population:</strong> 10,000+ (25% international)</p>
    <p><strong>Top Programs:</strong></p>
    <ul>
        <li>Business: #35 World</li>
        <li>Accounting: #25 World</li>
        <li>Law: #40 World</li>
        <li>Economics: #45 World</li>
    </ul>
    <p><strong>Tuition:</strong> SGD 25,000-35,000/year ($18,750-26,250 USD)</p>
    <p><strong>Teaching Style:</strong> Interactive seminar-style classes (40-50 students)</p>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ 2.4 Singapore University of Technology and Design (SUTD)</h3>
    <p><strong>Ranking:</strong> #4 Singapore, #151-200 World</p>
    <p><strong>Location:</strong> Changi, Singapore</p>
    <p><strong>Established:</strong> 2009</p>
    <p><strong>Specialization:</strong> Engineering, Architecture, Design, AI</p>
    <p><strong>Partner:</strong> Massachusetts Institute of Technology (MIT)</p>
    <p><strong>Tuition:</strong> SGD 22,000-32,000/year</p>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ 2.5 Singapore Institute of Technology (SIT)</h3>
    <p><strong>Ranking:</strong> #5 Singapore, #201-250 World</p>
    <p><strong>Location:</strong> Dover, Singapore</p>
    <p><strong>Established:</strong> 2009</p>
    <p><strong>Specialization:</strong> Applied learning with industry partnerships</p>
    <p><strong>Tuition:</strong> SGD 20,000-30,000/year</p>
</div>

<h2>3. University Comparison Table</h2>

<table class="comparison-table">
    <thead>
        <th>University</th>
        <th>World Rank</th>
        <th>Best For</th>
        <th>Tuition (SGD)</th>
        <th>Class Size</th>
    </thead>
    <tbody>
        <tr><td>NUS</td><td>#8</td><td>Research, Medicine, Law, CS</td><td>30,000-40,000</td><td>100-200</td></tr>
        <tr style="background:#f5f5f5;"><td>NTU</td><td>#12</td><td>Engineering, Materials, Design</td><td>28,000-38,000</td><td>80-150</td></tr>
        <tr><td>SMU</td><td>#87</td><td>Business, Economics, Law</td><td>25,000-35,000</td><td>40-50</td></tr>
        <tr style="background:#f5f5f5;"><td>SUTD</td><td>151-200</td><td>Engineering, Architecture, Design</td><td>22,000-32,000</td><td>30-40</td></tr>
        <tr><td>SIT</td><td>201-250</td><td>Applied Learning, Industry</td><td>20,000-30,000</td><td>25-35</td></tr>
    </tbody>
</table>

<h2>4. Admission Requirements</h2>

<h3>Undergraduate Programs</h3>
<ul>
    <li><strong>Academic:</strong> High school diploma with 90%+ marks</li>
    <li><strong>A-Levels:</strong> AAA/AAB for top universities</li>
    <li><strong>IB:</strong> 38+ points</li>
    <li><strong>SAT:</strong> 1400+ or ACT 32+ (recommended)</li>
    <li><strong>English:</strong> IELTS 6.5-7.0 or TOEFL 90+</li>
    <li><strong>Additional:</strong> Personal statement, 2 recommendation letters, interview for shortlisted candidates</li>
</ul>

<h3>Graduate Programs (Master's & PhD)</h3>
<ul>
    <li><strong>Master's by Coursework:</strong> Bachelor's degree (3.5/4.0 GPA), IELTS 6.5+, 2 years work experience recommended</li>
    <li><strong>Master's by Research:</strong> Bachelor's degree (3.0/4.0 GPA), strong research proposal, IELTS 6.5+</li>
    <li><strong>PhD:</strong> Master's degree, excellent research proposal, IELTS 7.0+, publications preferred</li>
    <li><strong>GRE/GMAT:</strong> Required for some programs (GRE 320+, GMAT 700+)</li>
</ul>

<h2>5. Scholarships Guide</h2>

<div class="scholarship-card">
    <h3>🎓 Singapore International Graduate Award (SINGA)</h3>
    <p><strong>Coverage:</strong> Full tuition + SGD 2,200/month stipend + SGD 1,500 airfare + SGD 1,000 settling-in allowance</p>
    <p><strong>Duration:</strong> Up to 4 years (PhD)</p>
    <p><strong>Deadline:</strong> June 1 & December 1</p>
    <p><strong>Eligibility:</strong> Outstanding international graduates for PhD in STEM fields</p>
    <p><strong>Partner Universities:</strong> NTU, NUS, SUTD, SIT, SMU</p>
</div>

<div class="scholarship-card">
    <h3>🎓 ASEAN Undergraduate Scholarship</h3>
    <p><strong>Coverage:</strong> Full tuition + SGD 5,800/year living allowance</p>
    <p><strong>Deadline:</strong> February-March</p>
    <p><strong>Eligibility:</strong> ASEAN citizens applying to NUS, NTU, SMU</p>
</div>

<div class="scholarship-card">
    <h3>🎓 NUS Merit Scholarship</h3>
    <p><strong>Coverage:</strong> Full tuition + SGD 5,800/year living allowance + accommodation</p>
    <p><strong>Eligibility:</strong> Outstanding academic record, leadership qualities</p>
</div>

<div class="scholarship-card">
    <h3>🎓 NTU Nanyang Scholarship</h3>
    <p><strong>Coverage:</strong> Full tuition + SGD 5,000/year living allowance + accommodation</p>
    <p><strong>Eligibility:</strong> Top 5% of applicants</p>
</div>

<div class="scholarship-card">
    <h3>🎓 SMU Global Impact Scholarship</h3>
    <p><strong>Coverage:</strong> Full tuition + SGD 5,000/year living allowance</p>
    <p><strong>Eligibility:</strong> Strong academic record, leadership experience</p>
</div>

<h2>6. Cost of Living Breakdown</h2>

<h3>Accommodation Options</h3>
<ul>
    <li><strong>University Dormitory (single):</strong> SGD 400-800/month</li>
    <li><strong>University Dormitory (twin):</strong> SGD 250-500/month</li>
    <li><strong>HDB Flat (shared room):</strong> SGD 800-1,200/month</li>
    <li><strong>Private Apartment (studio):</strong> SGD 1,500-2,500/month</li>
    <li><strong>Condo (private room):</strong> SGD 1,000-1,800/month</li>
</ul>

<h3>Food Expenses</h3>
<ul>
    <li><strong>Hawker Center:</strong> SGD 3-6/meal (best value!)</li>
    <li><strong>Food Court:</strong> SGD 5-8/meal</li>
    <li><strong>Restaurant:</strong> SGD 15-30/meal</li>
    <li><strong>Groceries:</strong> SGD 200-300/month</li>
</ul>

<h3>Transportation</h3>
<ul>
    <li><strong>MRT/Bus:</strong> SGD 1.50-2.50/trip</li>
    <li><strong>Student Monthly Pass:</strong> SGD 50-100</li>
    <li><strong>Taxi/Grab:</strong> SGD 10-25/trip</li>
</ul>

<table class="cost-table">
    <thead>
        <th>Expense</th>
        <th>Budget Student</th>
        <th>Moderate Student</th>
        <th>Comfortable Student</th>
    </thead>
    <tbody>
        <tr><td>Accommodation</td><td>SGD 400-600</td><td>SGD 800-1,200</td><td>SGD 1,500-2,500</td></tr>
        <tr><td>Food</td><td>SGD 300-400</td><td>SGD 400-600</td><td>SGD 600-800</td></tr>
        <tr><td>Transport</td><td>SGD 50-80</td><td>SGD 80-120</td><td>SGD 150-200</td></tr>
        <tr><td>Utilities</td><td>SGD 50-80</td><td>SGD 80-120</td><td>SGD 150-200</td></tr>
        <tr><td>Entertainment</td><td>SGD 100-150</td><td>SGD 150-250</td><td>SGD 300-500</td></tr>
        <tr style="background:#D4AF37; font-weight:bold;"><td>TOTAL</td><td>SGD 900-1,310</td><td>SGD 1,510-2,290</td><td>SGD 2,700-4,200</td></tr>
    </tbody>
</table>

<h2>7. Student Visa Process (Student's Pass)</h2>

<div class="timeline">
    <div class="timeline-step">
        <div class="timeline-number">1</div>
        <strong>Get Admission</strong>
        <p>Receive offer letter</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">2</div>
        <strong>SOLAR Registration</strong>
        <p>University registers you</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">3</div>
        <strong>Apply Online</strong>
        <p>2-4 weeks processing</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">4</div>
        <strong>Medical Check</strong>
        <p>In Singapore</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">5</div>
        <strong>Collect Student Pass</strong>
        <p>At ICA</p>
    </div>
</div>

<div class="tip-box">
    <h3>💡 Pro Tips for Singapore</h3>
    <ul>
        <li>Eat at hawker centers – affordable and authentic Singaporean cuisine</li>
        <li>Use the MRT – fastest and most convenient way to get around</li>
        <li>Join orientation week to make friends and learn about campus life</li>
        <li>Explore nearby countries on weekends (Malaysia, Indonesia, Thailand)</li>
        <li>Respect local customs – Singapore is a multicultural society</li>
        <li>Apply for scholarships early – deadlines are February-March</li>
    </ul>
</div>

<div class="tip-box" style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white;">
    <h2 style="color: white;">🎓 Your Singapore Journey Starts Here!</h2>
    <p style="font-size: 18px;">With world-class universities, generous scholarships, and unlimited opportunities, Singapore is waiting for you!</p>
    <p><strong>Start your application today! 🇸🇬</strong></p>
</div>
'''

# Update Article 14 (Singapore Universities)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 14", (singapore_guide_content,))
print("✅ Updated Singapore Guide article (ID 14)")

# Also update Article 15 (Singapore Scholarships) with same content
c.execute("UPDATE blog_posts SET content = ? WHERE id = 15", (singapore_guide_content,))
print("✅ Updated Singapore Scholarships article (ID 15)")

conn.commit()
conn.close()
import sqlite3

conn = sqlite3.connect('applications.db')
c = conn.cursor()

# ==================== ARTICLE 11: MALAYSIA (Already updated - keeping for reference) ====================
# Your existing Malaysia content here (keeping what you already have)

# ==================== ARTICLE 8 & 22: JAPANESE UNIVERSITY ENTRANCE EXAMS - COMPLETE GUIDE ====================
japan_exams_content = '''
<style>
.exam-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2D4FA8 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}
.exam-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: linear-gradient(135deg, #D4AF37, #F3D03E);
    color: #1E3A8A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.eju-section {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #D4AF37;
}
.score-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.score-table th {
    background: #1E3A8A;
    color: white;
    padding: 12px;
    text-align: left;
}
.score-table td {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}
.university-card {
    background: #EFF6FF;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
}
.timeline {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
    margin: 30px 0;
}
.timeline-step {
    flex: 1;
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}
.timeline-number {
    background: #D4AF37;
    color: #1E3A8A;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin: 0 auto 15px;
}
.jlpt-box {
    background: #EFF6FF;
    border-left: 4px solid #D4AF37;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
.prep-tips {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin: 20px 0;
}
.tip-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}
</style>

<div class="exam-header">
    <h1 style="color: white; font-size: 36px;">📚 Complete Guide to Japanese University Entrance Exams</h1>
    <p style="font-size: 18px;">EJU, JLPT, and University-Specific Exams – Your Path to Japanese Universities</p>
</div>

<div class="exam-stats">
    <div class="stat-card">
        <div class="stat-number">280+</div>
        <div>Universities Accepting EJU</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">2x/Year</div>
        <div>EJU Exam Schedule</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">800+</div>
        <div>Test Centers Worldwide</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">50,000+</div>
        <div>Annual Test Takers</div>
    </div>
</div>

<h2>📖 Table of Contents</h2>
<ul>
    <li>1. Overview: Japanese University Entrance System</li>
    <li>2. EJU (Examination for Japanese University Admission) – Complete Guide</li>
    <li>3. EJU Subjects Breakdown</li>
    <li>4. EJU Score Requirements by University</li>
    <li>5. JLPT (Japanese-Language Proficiency Test) Guide</li>
    <li>6. University-Specific Entrance Exams</li>
    <li>7. Top Universities and Their Requirements</li>
    <li>8. Application Timeline for Japanese Universities</li>
    <li>9. Preparation Strategies and Study Resources</li>
    <li>10. Tips from Successful Applicants</li>
    <li>11. Frequently Asked Questions</li>
</ul>

<h2>1. Overview: Japanese University Entrance System</h2>

<div class="jlpt-box">
    <p>Japanese universities use a multi-stage admission process for international students. Most universities require:</p>
    <ul>
        <li><strong>Step 1:</strong> EJU (Examination for Japanese University Admission) or JLPT scores</li>
        <li><strong>Step 2:</strong> University-specific entrance exams and interviews</li>
        <li><strong>Step 3:</strong> Document screening and final selection</li>
    </ul>
</div>

<h2>2. EJU (Examination for Japanese University Admission) – Complete Guide</h2>

<div class="eju-section">
    <h3 style="color: #1E3A8A;">What is the EJU?</h3>
    <p>The EJU is the standard entrance exam for international students applying to Japanese universities. Held twice a year (June and November) in Japan and 14 other countries, it evaluates Japanese language ability and basic academic skills needed for university study.</p>
    
    <h3>📅 Test Dates & Locations</h3>
    <ul>
        <li><strong>June Examination:</strong> 3rd Sunday of June</li>
        <li><strong>November Examination:</strong> 2nd Sunday of November</li>
        <li><strong>Test Centers:</strong> Japan, India, Indonesia, Malaysia, Mongolia, Myanmar, Philippines, South Korea, Sri Lanka, Taiwan, Thailand, Vietnam, and more</li>
        <li><strong>Registration:</strong> 2-3 months before exam date</li>
    </ul>
</div>

<h2>3. EJU Subjects Breakdown</h2>

<h3>📖 Japanese as a Foreign Language</h3>
<div class="score-table">
    <table style="width:100%; border-collapse:collapse;">
        <tr style="background:#1E3A8A; color:white;">
            <th>Section</th>
            <th>Duration</th>
            <th>Score Range</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>Reading Comprehension</td>
            <td>40 min</td>
            <td>0-200 points</td>
            <td>Academic texts, graphs, advertisements</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td>Listening Comprehension</td>
            <td>30 min</td>
            <td>0-200 points</td>
            <td>Lectures, conversations, announcements</td>
        </tr>
        <tr>
            <td>Listening-Reading Comprehension</td>
            <td>55 min</td>
            <td>0-200 points</td>
            <td>Integrated audio and text materials</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td>Writing (Essay)</td>
            <td>30 min</td>
            <td>0-50 points</td>
            <td>Opinion essay on academic topics</td>
        </tr>
    </table>
</div>

<h3>🔬 Science (Choose 2 subjects)</h3>
<ul>
    <li><strong>Physics:</strong> Mechanics, thermodynamics, waves, electricity, magnetism</li>
    <li><strong>Chemistry:</strong> Atomic structure, chemical reactions, organic chemistry</li>
    <li><strong>Biology:</strong> Cell biology, genetics, evolution, ecology</li>
</ul>
<p><strong>Duration:</strong> 80 minutes | <strong>Score:</strong> 0-200 points</p>

<h3>📐 Mathematics</h3>
<ul>
    <li><strong>Course 1:</strong> For humanities and social sciences (equations, functions, probability)</li>
    <li><strong>Course 2:</strong> For sciences and engineering (calculus, vectors, matrices, complex numbers)</li>
</ul>
<p><strong>Duration:</strong> 80 minutes | <strong>Score:</strong> 0-200 points</p>

<h3>🌏 Japan and the World</h3>
<p><strong>Topics:</strong> Modern Japan, world history, geography, economics, politics, international relations</p>
<p><strong>Duration:</strong> 80 minutes | <strong>Score:</strong> 0-200 points</p>

<h2>4. EJU Score Requirements by University</h2>

<div class="score-table">
    <table style="width:100%; border-collapse:collapse;">
        <tr style="background:#1E3A8A; color:white;">
            <th>University</th>
            <th>Required EJU Score</th>
            <th>Japanese Section</th>
            <th>Subject Requirements</th>
        </tr>
        <tr>
            <td><strong>University of Tokyo</strong></td>
            <td>680+</td>
            <td>300+ (Reading + Listening)</td>
            <td>Science: 2 subjects + Math 2</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>Kyoto University</strong></td>
            <td>650+</td>
            <td>280+</td>
            <td>Science: 2 subjects + Math 2</td>
        </tr>
        <tr>
            <td><strong>Osaka University</strong></td>
            <td>620+</td>
            <td>270+</td>
            <td>Science: 2 subjects + Math 2</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>Tohoku University</strong></td>
            <td>600+</td>
            <td>260+</td>
            <td>Science: 2 subjects + Math 2</td>
        </tr>
        <tr>
            <td><strong>Tokyo Institute of Technology</strong></td>
            <td>650+</td>
            <td>Not required (English programs)</td>
            <td>Math 2 + Science (2 subjects)</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>Waseda University</strong></td>
            <td>580+</td>
            <td>250+</td>
            <td>Varies by department</td>
        </tr>
        <tr>
            <td><strong>Keio University</strong></td>
            <td>600+</td>
            <td>260+</td>
            <td>Varies by department</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>Nagoya University</strong></td>
            <td>600+</td>
            <td>260+</td>
            <td>Science: 2 subjects + Math 2</td>
        </tr>
        <tr>
            <td><strong>Hokkaido University</strong></td>
            <td>580+</td>
            <td>250+</td>
            <td>Varies by department</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>Kyushu University</strong></td>
            <td>580+</td>
            <td>250+</td>
            <td>Varies by department</td>
        </tr>
    </table>
</div>

<h2>5. JLPT (Japanese-Language Proficiency Test) Guide</h2>

<div class="jlpt-box">
    <h3>What is the JLPT?</h3>
    <p>The JLPT measures Japanese language ability for non-native speakers. Many universities accept JLPT in place of EJU Japanese section.</p>
</div>

<div class="score-table">
    <table style="width:100%; border-collapse:collapse;">
        <tr style="background:#1E3A8A; color:white;">
            <th>Level</th>
            <th>Vocabulary</th>
            <th>Kanji</th>
            <th>Study Hours</th>
            <th>Can Do</th>
        </tr>
        <tr>
            <td><strong>N5</strong></td>
            <td>800 words</td>
            <td>100 characters</td>
            <td>150-250 hours</td>
            <td>Basic daily expressions</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>N4</strong></td>
            <td>1,500 words</td>
            <td>300 characters</td>
            <td>300-400 hours</td>
            <td>Everyday conversations</td>
        </tr>
        <tr>
            <td><strong>N3</strong></td>
            <td>3,750 words</td>
            <td>650 characters</td>
            <td>450-600 hours</td>
            <td>Basic life and study situations</td>
        </tr>
        <tr style="background:#f5f5f5;">
            <td><strong>N2</strong></td>
            <td>6,000 words</td>
            <td>1,000 characters</td>
            <td>600-800 hours</td>
            <td>Required for most universities</td>
        </tr>
        <tr>
            <td><strong>N1</strong></td>
            <td>10,000 words</td>
            <td>2,000 characters</td>
            <td>900+ hours</td>
            <td>Near-native fluency</td>
        </tr>
    </table>
</div>

<h2>6. University-Specific Entrance Exams</h2>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ University of Tokyo</h3>
    <ul>
        <li><strong>First Screening:</strong> EJU scores (680+) or JLPT N1</li>
        <li><strong>Second Screening:</strong> Written exam (subject-specific)</li>
        <li><strong>Third Screening:</strong> Interview (Japanese and English)</li>
        <li><strong>English Proficiency:</strong> TOEFL iBT 90+ or IELTS 6.5+ required</li>
    </ul>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ Kyoto University</h3>
    <ul>
        <li><strong>First Screening:</strong> EJU scores (650+) or JLPT N1</li>
        <li><strong>Second Screening:</strong> Department-specific written exam</li>
        <li><strong>Third Screening:</strong> Interview with faculty</li>
        <li><strong>English Proficiency:</strong> TOEFL iBT 85+ or IELTS 6.5+</li>
    </ul>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ Waseda University</h3>
    <ul>
        <li><strong>First Screening:</strong> EJU scores (580+) or JLPT N2+</li>
        <li><strong>Second Screening:</strong> Essay writing + Interview</li>
        <li><strong>English Proficiency:</strong> TOEFL iBT 80+ (for some programs)</li>
        <li><strong>Portfolio:</strong> Required for art and design programs</li>
    </ul>
</div>

<div class="university-card">
    <h3 style="color: #1E3A8A;">🏛️ Tokyo Institute of Technology</h3>
    <ul>
        <li><strong>First Screening:</strong> EJU scores (Math 2 + Science) or SAT/ACT</li>
        <li><strong>Second Screening:</strong> English-taught program exam</li>
        <li><strong>Interview:</strong> Video interview for international applicants</li>
        <li><strong>English Proficiency:</strong> TOEFL iBT 80+ or IELTS 6.0+</li>
    </ul>
</div>

<h2>7. Application Timeline for Japanese Universities</h2>

<div class="timeline">
    <div class="timeline-step">
        <div class="timeline-number">1</div>
        <strong>April-June</strong>
        <p>Take EJU (June)</p>
        <p>Prepare documents</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">2</div>
        <strong>July-August</strong>
        <p>Submit applications</p>
        <p>First screening results</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">3</div>
        <strong>September-October</strong>
        <p>University exams</p>
        <p>Interviews</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">4</div>
        <strong>November-December</strong>
        <p>Final results</p>
        <p>Visa application</p>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">5</div>
        <strong>April</strong>
        <p>Enrollment</p>
        <p>Begin studies</p>
    </div>
</div>

<h2>8. Preparation Strategies and Study Resources</h2>

<div class="prep-tips">
    <div class="tip-card">
        <h3 style="color: #1E3A8A;">📚 Recommended Books</h3>
        <ul>
            <li>EJU Official Practice Questions (JASSO)</li>
            <li>Understanding Japanese University Entrance Exams</li>
            <li>EJU Mathematics Course 1 & 2</li>
            <li>EJU Science (Physics, Chemistry, Biology)</li>
            <li>Japan and the World Study Guide</li>
        </ul>
    </div>
    <div class="tip-card">
        <h3 style="color: #1E3A8A;">📱 Online Resources</h3>
        <ul>
            <li>JASSO Official Website (eju.jasso.go.jp)</li>
            <li>EJU Past Papers Online</li>
            <li>YouTube: EJU Preparation Channels</li>
            <li>Japanese Study Apps: Anki, Bunpo</li>
        </ul>
    </div>
    <div class="tip-card">
        <h3 style="color: #1E3A8A;">📝 Study Plan</h3>
        <ul>
            <li><strong>6 months before:</strong> Start intensive Japanese study</li>
            <li><strong>3 months before:</strong> Practice past exams</li>
            <li><strong>1 month before:</strong> Mock tests, time management</li>
            <li><strong>Weekly:</strong> 2-3 full practice sets</li>
        </ul>
    </div>
    <div class="tip-card">
        <h3 style="color: #1E3A8A;">🎯 Test-Taking Tips</h3>
        <ul>
            <li>Practice time management (strict timing)</li>
            <li>Read instructions carefully</li>
            <li>Answer all questions (no penalty for wrong answers)</li>
            <li>Stay calm and focused</li>
        </ul>
    </div>
</div>

<h2>9. Tips from Successful Applicants</h2>

<div class="jlpt-box">
    <h3>🌟 "How I Got into University of Tokyo" – Sarah, NUS Graduate</h3>
    <ul>
        <li><strong>EJU Score:</strong> 720 (Japanese 340, Math 2 180, Physics 200)</li>
        <li><strong>Preparation:</strong> 1 year of intensive study, 20 hours/week</li>
        <li><strong>Key Strategy:</strong> Practiced 10 years of past EJU exams</li>
        <li><strong>Interview Tip:</strong> Showed passion for my research field</li>
    </ul>
</div>

<div class="jlpt-box">
    <h3>🌟 "Waseda University Success Story" – David, International Student</h3>
    <ul>
        <li><strong>Strategy:</strong> Focused on Japanese reading comprehension</li>
        <li><strong>Resource:</strong> Read NHK News Easy daily</li>
        <li><strong>Speaking Practice:</strong> 2 hours/week with language partner</li>
        <li><strong>Advice:</strong> Start early and stay consistent</li>
    </ul>
</div>

<h2>10. Frequently Asked Questions</h2>

<div class="jlpt-box">
    <h3>❓ Do I need to take both EJU and JLPT?</h3>
    <p>Most universities require EJU. Some accept JLPT as a substitute for the Japanese section. Check individual university requirements.</p>
    
    <h3>❓ How long are EJU scores valid?</h3>
    <p>EJU scores are valid for 2 years. Most universities accept scores from the past 2-3 exam sessions.</p>
    
    <h3>❓ Can I take EJU outside Japan?</h3>
    <p>Yes! EJU is offered in 14 countries including India, Indonesia, Malaysia, Thailand, Vietnam, South Korea, and Taiwan.</p>
    
    <h3>❓ What's the passing score for EJU?</h3>
    <p>There's no passing or failing score. Universities set their own minimum requirements. Higher scores increase admission chances.</p>
    
    <h3>❓ Do English-taught programs require EJU?</h3>
    <p>Some English-taught programs don't require EJU. Instead, they may require SAT/ACT, IB, or A-Levels. Check university websites.</p>
    
    <h3>❓ How many times can I take EJU?</h3>
    <p>Unlimited. You can take EJU as many times as you want. Most students take it twice (June and November) and submit the best score.</p>
</div>

<div style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); padding: 40px; border-radius: 20px; text-align: center; margin-top: 30px; color: white;">
    <h2 style="color: white;">🎓 Ready to Ace the Japanese University Entrance Exams?</h2>
    <p style="font-size: 18px;">With dedicated preparation and the right strategy, you can succeed in EJU and gain admission to Japan's top universities!</p>
    <p><strong>Start your preparation today! 🇯🇵</strong></p>
</div>
'''

# Update Article 8 (Japanese University Entrance Exams Explained)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 8", (japan_exams_content,))
print("✅ Updated Japanese Entrance Exams article (ID 8)")

# Also update Article 22 (EJU Exam)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 22", (japan_exams_content,))
print("✅ Updated EJU Exam article (ID 22)")

# ==================== ARTICLE 17: KOREA - ULTRA DETAILED ====================
korea_content = '''
<h1>🇰🇷 Complete Guide to Studying in South Korea: Top Universities, KGSP, TOPIK & More</h1>

<div class="info-box">
<h3>📊 Quick Overview</h3>
<ul>
<li>🏛️ 50+ Universities (SNU #29, KAIST #41, Yonsei #73)</li>
<li>🌏 200,000+ International Students</li>
<li>💰 Tuition: KRW 5,000,000-9,000,000/year ($3,800-6,800 USD)</li>
<li>🏠 Living Cost: KRW 800,000-1,500,000/month ($600-1,100 USD)</li>
<li>📚 Korean/English Medium Instruction</li>
<li>🎓 K-Wave Culture | World-Class Technology</li>
</ul>
</div>

<h2>📖 Table of Contents</h2>
<ul>
<li>1. Why Study in Korea?</li>
<li>2. Top 30 Universities in Korea</li>
<li>3. Detailed University Profiles</li>
<li>4. Admission Requirements (TOPIK)</li>
<li>5. Tuition Fees by University</li>
<li>6. KGSP Scholarship Guide</li>
<li>7. Cost of Living Breakdown</li>
<li>8. Student Visa Process (D-2)</li>
<li>9. Student Life & Culture</li>
<li>10. Career Opportunities in Korea</li>
<li>11. Frequently Asked Questions</li>
</ul>

<h2>1. Why Study in South Korea?</h2>
<p>South Korea has emerged as a global leader in education, technology, and innovation. With world-class universities, cutting-edge research, and the global K-Wave (Hallyu), Korea attracts over 200,000 international students annually.</p>

<h3>1.1 Academic Excellence</h3>
<p>Korean universities rank among the world's best. Seoul National University (#29), KAIST (#41), and Yonsei (#73) are globally recognized for their research and teaching excellence.</p>

<h3>1.2 Technological Innovation</h3>
<p>Korea invests 4.8% of GDP in R&D (2nd highest in the world). Home to global tech giants like Samsung, LG, and SK Hynix, offering unparalleled opportunities in STEM fields.</p>

<h3>1.3 Korean Wave (Hallyu)</h3>
<p>From K-pop (BTS, BLACKPINK) to K-dramas, Korean culture is globally popular. Studying in Korea offers immersive cultural experiences.</p>

<h3>1.4 Safety and Infrastructure</h3>
<p>Korea is extremely safe, with 24-hour public transport, fast internet, and modern infrastructure. Seoul is one of the world's most connected cities.</p>

<h2>2. Top 30 Universities in Korea</h2>

<h3>2.1 Seoul National University (SNU)</h3>
<p><strong>Ranking:</strong> #1 Korea, #29 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Established:</strong> 1946</p>
<p><strong>Student Population:</strong> 28,000+ (10% international)</p>
<p><strong>Top Programs:</strong> Engineering (#20 World), Business (#30 World), Medicine (#25 World), Law (#15 World)</p>
<p><strong>Tuition:</strong> KRW 5,000,000-7,000,000/year ($3,800-5,300 USD)</p>
<p><strong>Notable Alumni:</strong> 3 Korean Presidents, Business Leaders, Nobel Laureates</p>

<h3>2.2 KAIST (Korea Advanced Institute of Science and Technology)</h3>
<p><strong>Ranking:</strong> #2 Korea, #41 World</p>
<p><strong>Location:</strong> Daejeon</p>
<p><strong>Established:</strong> 1971</p>
<p><strong>Student Population:</strong> 10,000+ (15% international)</p>
<p><strong>Top Programs:</strong> Electrical Engineering (#15 World), Computer Science (#20 World), Mechanical Engineering (#25 World)</p>
<p><strong>Tuition:</strong> KRW 6,000,000-8,000,000/year</p>
<p><strong>Known as:</strong> "MIT of Asia"</p>

<h3>2.3 Yonsei University</h3>
<p><strong>Ranking:</strong> #3 Korea, #73 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Established:</strong> 1885</p>
<p><strong>Student Population:</strong> 26,000+ (18% international)</p>
<p><strong>Top Programs:</strong> Business (#35 World), Medicine (#40 World), Engineering (#70 World)</p>
<p><strong>Tuition:</strong> KRW 7,000,000-9,000,000/year</p>

<h3>2.4 Korea University</h3>
<p><strong>Ranking:</strong> #4 Korea, #74 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Established:</strong> 1905</p>
<p><strong>Top Programs:</strong> Law (#50 World), Political Science (#45 World), Business (#60 World)</p>
<p><strong>Tuition:</strong> KRW 7,000,000-9,000,000/year</p>

<h3>2.5 POSTECH (Pohang University of Science and Technology)</h3>
<p><strong>Ranking:</strong> #5 Korea, #81 World</p>
<p><strong>Location:</strong> Pohang</p>
<p><strong>Established:</strong> 1986</p>
<p><strong>Top Programs:</strong> Materials Science (#10 World), Computer Science (#50 World), Physics (#60 World)</p>
<p><strong>Tuition:</strong> KRW 6,000,000-8,000,000/year</p>

<h3>2.6 Sungkyunkwan University (SKKU)</h3>
<p><strong>Ranking:</strong> #6 Korea, #97 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Established:</strong> 1398 (modern 1945)</p>
<p><strong>Partner:</strong> Samsung</p>
<p><strong>Top Programs:</strong> Business (#80 World), Engineering (#90 World), Medicine</p>

<h3>2.7 Hanyang University</h3>
<p><strong>Ranking:</strong> #7 Korea, #104 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Top Programs:</strong> Engineering (#70 World), Architecture (#40 World), Business</p>

<h3>2.8 Kyung Hee University</h3>
<p><strong>Ranking:</strong> #8 Korea, #236 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Top Programs:</strong> Medicine (#150 World), Hospitality (#30 World), Business</p>

<h3>2.9 Ewha Womans University</h3>
<p><strong>Ranking:</strong> #9 Korea, #318 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Top Programs:</strong> Medicine, Law, Business, Education, Arts</p>
<p><strong>Note:</strong> Top women's university in Asia</p>

<h3>2.10 Sogang University</h3>
<p><strong>Ranking:</strong> #10 Korea, #490 World</p>
<p><strong>Location:</strong> Seoul</p>
<p><strong>Top Programs:</strong> Business, Economics, Engineering, Computer Science</p>

<h3>More Top Universities (11-30)</h3>
<ul>
<li>11. University of Seoul</li>
<li>12. Chung-Ang University</li>
<li>13. Dongguk University</li>
<li>14. Hongik University (Arts & Design)</li>
<li>15. Konkuk University</li>
<li>16. Inha University</li>
<li>17. Ajou University</li>
<li>18. Sejong University</li>
<li>19. Kookmin University</li>
<li>20. Sookmyung Women's University</li>
<li>21. Pusan National University (Busan)</li>
<li>22. Kyungpook National University (Daegu)</li>
<li>23. Chonnam National University (Gwangju)</li>
<li>24. Chungnam National University (Daejeon)</li>
<li>25. Jeonbuk National University (Jeonju)</li>
<li>26. Gyeongsang National University (Jinju)</li>
<li>27. Kangwon National University (Chuncheon)</li>
<li>28. Cheju National University (Jeju Island)</li>
<li>29. Dankook University</li>
<li>30. Catholic University of Korea</li>
</ul>

<h2>3. Detailed University Profiles</h2>

<h3>3.1 Seoul National University - In-Depth</h3>
<p><strong>Faculties:</strong> 16 colleges, 1 graduate school</p>
<ul>
<li>College of Humanities</li>
<li>College of Social Sciences</li>
<li>College of Natural Sciences</li>
<li>College of Nursing</li>
<li>College of Business Administration</li>
<li>College of Engineering (11 departments)</li>
<li>College of Agriculture and Life Sciences</li>
<li>College of Law (Top law school in Korea)</li>
<li>College of Medicine (Korea's best medical school)</li>
<li>College of Pharmacy</li>
<li>College of Music</li>
<li>College of Fine Arts</li>
</ul>
<p><strong>Research Centers:</strong> 100+ research institutes including the Institute for Advanced Study, Nano Systems Institute, and Cancer Research Institute.</p>

<h3>3.2 KAIST - In-Depth</h3>
<p><strong>Schools:</strong></p>
<ul>
<li>College of Natural Sciences</li>
<li>College of Life Science & Bioengineering</li>
<li>College of Engineering (8 departments)</li>
<li>College of Business</li>
<li>School of Computing (Top CS program in Korea)</li>
<li>Graduate School of AI</li>
<li>Graduate School of Data Science</li>
</ul>
<p><strong>Research Excellence:</strong> 20 research centers including the Institute for AI, Robotics Institute, and Quantum Computing Center.</p>

<h2>4. Admission Requirements</h2>

<h3>TOPIK (Test of Proficiency in Korean)</h3>
<p>TOPIK is required for Korean-taught programs:</p>
<ul>
<li><strong>TOPIK 3:</strong> Everyday conversation (required for some universities)</li>
<li><strong>TOPIK 4:</strong> General academic study (required for most undergraduate)</li>
<li><strong>TOPIK 5:</strong> Advanced academic study (required for graduate)</li>
<li><strong>TOPIK 6:</strong> Professional proficiency (research, specialized fields)</li>
</ul>

<h3>English-Taught Programs Requirements</h3>
<ul>
<li>IELTS 6.0-6.5 or TOEFL 80-90</li>
<li>SAT 1300+ (recommended)</li>
<li>Strong academic records (GPA 3.5+)</li>
</ul>

<h3>Application Deadlines</h3>
<ul>
<li>Fall Intake (September): April-May application</li>
<li>Spring Intake (March): October-November application</li>
</ul>

<h2>5. Tuition Fees by University</h2>
<ul>
<li>SNU: KRW 5,000,000-7,000,000/year</li>
<li>KAIST: KRW 6,000,000-8,000,000/year</li>
<li>Yonsei: KRW 7,000,000-9,000,000/year</li>
<li>Korea University: KRW 7,000,000-9,000,000/year</li>
<li>POSTECH: KRW 6,000,000-8,000,000/year</li>
<li>SKKU: KRW 7,000,000-9,000,000/year</li>
<li>Hanyang: KRW 7,000,000-9,000,000/year</li>
<li>Private Universities: KRW 8,000,000-12,000,000/year</li>
</ul>

<h2>6. KGSP Scholarship Guide</h2>

<h3>KGSP Benefits</h3>
<ul>
<li><strong>Full tuition</strong> for entire program</li>
<li><strong>Monthly stipend:</strong> KRW 900,000-1,000,000</li>
<li><strong>Korean language training:</strong> 1 year at leading language institutes</li>
<li><strong>Round-trip airfare</strong> (economy class)</li>
<li><strong>Medical insurance:</strong> 80% coverage</li>
<li><strong>Settlement allowance:</strong> KRW 200,000 upon arrival</li>
<li><strong>Research support:</strong> KRW 210,000-240,000 for graduate students</li>
</ul>

<h3>Two Application Tracks</h3>
<p><strong>Track A (Embassy):</strong> Apply through Korean embassy in your country. Deadline: February-March. 1-5 students per country.</p>
<p><strong>Track B (University):</strong> Apply directly to Korean universities. Deadline: March-April. More spots available.</p>

<h3>Eligibility</h3>
<ul>
<li><strong>Undergraduate:</strong> High school graduate, under 25, GPA 80%+</li>
<li><strong>Graduate:</strong> Bachelor's degree, under 40, GPA 80%+</li>
<li>Good physical and mental health</li>
<li>Strong academic record (top 20% of class)</li>
</ul>

<h2>7. Cost of Living Breakdown</h2>

<h3>Accommodation</h3>
<ul>
<li>University dormitory: KRW 300,000-500,000/month</li>
<li>Goshiwon (cheap room): KRW 300,000-500,000/month</li>
<li>One-room apartment: KRW 500,000-800,000/month</li>
<li>Share house: KRW 400,000-600,000/month</li>
<li>Housing deposit: KRW 5,000,000-10,000,000 (returnable)</li>
</ul>

<h3>Food Expenses</h3>
<ul>
<li>University cafeteria: KRW 4,000-6,000 per meal</li>
<li>Korean BBQ: KRW 15,000-25,000 per person</li>
<li>Street food: KRW 2,000-5,000</li>
<li>Groceries: KRW 300,000-500,000/month</li>
</ul>

<h3>Transportation</h3>
<ul>
<li>Subway/bus: KRW 1,250-2,000 per trip</li>
<li>Monthly transport pass: KRW 50,000-80,000</li>
<li>Taxi: KRW 3,800-10,000 per trip</li>
</ul>

<h3>Monthly Budget Summary</h3>
<ul>
<li><strong>Budget Student:</strong> KRW 700,000-900,000 ($520-670)</li>
<li><strong>Moderate Student:</strong> KRW 900,000-1,200,000 ($670-900)</li>
<li><strong>Comfortable Student:</strong> KRW 1,200,000-1,500,000 ($900-1,120)</li>
</ul>

<h2>8. Student Visa Process (D-2)</h2>
<h3>Types of D-2 Visas</h3>
<ul>
<li>D-2-1: Associate degree</li>
<li>D-2-2: Bachelor's degree</li>
<li>D-2-3: Master's degree</li>
<li>D-2-4: Doctoral degree</li>
<li>D-2-5: Research programs</li>
<li>D-2-6: Exchange programs</li>
</ul>

<h3>Step-by-Step Process</h3>
<p><strong>Step 1:</strong> Get admission from Korean university</p>
<p><strong>Step 2:</strong> Prepare documents: passport, admission letter, financial proof ($10,000+), transcripts, study plan</p>
<p><strong>Step 3:</strong> Apply at Korean embassy (processing 7-14 days)</p>
<p><strong>Step 4:</strong> Enter Korea, get Alien Registration Card within 90 days</p>

<h2>9. Student Life & Culture</h2>
<h3>Festivals</h3>
<ul>
<li>Lunar New Year (Seollal): January/February</li>
<li>Cherry Blossom Festival: April</li>
<li>Buddha's Birthday (Lotus Lantern Festival): May</li>
<li>Chuseok (Korean Thanksgiving): September/October</li>
<li>University festivals (Daedongje): May/September</li>
</ul>

<h3>Student Activities</h3>
<ul>
<li>Club activities: Sports, music, dance, volunteer, language exchange</li>
<li>MT (Membership Training): Overnight retreats with classmates</li>
<li>Noraebang (karaoke): Popular social activity</li>
<li>PC Bang: Gaming cafes</li>
<li>Jjimjilbang: Korean sauna/spa</li>
</ul>

<h2>10. Career Opportunities</h2>
<h3>Top Employers</h3>
<ul>
<li>Technology: Samsung, LG, SK Hynix, Naver, Kakao</li>
<li>Automotive: Hyundai, Kia</li>
<li>Finance: Shinhan, KB, Hana, Woori Bank</li>
<li>Entertainment: SM, JYP, YG Entertainment</li>
</ul>

<h3>Average Starting Salaries</h3>
<ul>
<li>Engineering: KRW 40,000,000-55,000,000/year</li>
<li>Computer Science: KRW 45,000,000-60,000,000/year</li>
<li>Business/Finance: KRW 35,000,000-50,000,000/year</li>
<li>Research: KRW 38,000,000-52,000,000/year</li>
</ul>

<h2>11. Frequently Asked Questions</h2>
<h3>Q1: Can I work while studying?</h3>
<p>Yes, up to 20 hours/week during semester, full-time during breaks (with permission).</p>
<h3>Q2: Do I need TOPIK?</h3>
<p>For Korean programs, TOPIK 3-4 required. English programs need IELTS/TOEFL.</p>
<h3>Q3: Is Korea safe?</h3>
<p>Yes, Korea is very safe with low crime rates. Women feel safe walking alone at night.</p>
<h3>Q4: Can I stay after graduation?</h3>
<p>Yes, graduates can apply for D-10 Job Seeker Visa (up to 2 years) to find employment.</p>
'''

c.execute("UPDATE blog_posts SET content = ? WHERE id = 17", (korea_content,))
print("✅ Updated Korea article (ID 17)")

# ==================== ARTICLE 28: STUDENT LIFE IN ASIA - COMPLETE GUIDE ====================
student_life_content = '''
<style>
.life-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2D4FA8 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}
.life-stats {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: linear-gradient(135deg, #D4AF37, #F3D03E);
    color: #1E3A8A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.country-tab {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 30px 0;
}
.tab-btn {
    background: white;
    border: 2px solid #1E3A8A;
    padding: 12px 25px;
    border-radius: 40px;
    color: #1E3A8A;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}
.tab-btn:hover, .tab-btn.active {
    background: #1E3A8A;
    color: white;
}
.country-card {
    background: white;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-left: 5px solid #D4AF37;
    display: none;
}
.country-card.active {
    display: block;
}
.country-title {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}
.country-title .flag {
    font-size: 48px;
}
.country-title h2 {
    color: #1E3A8A;
    font-size: 32px;
    margin: 0;
}
.life-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    margin: 25px 0;
}
.life-card {
    background: #EFF6FF;
    padding: 20px;
    border-radius: 15px;
}
.life-card h3 {
    color: #1E3A8A;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.cost-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.cost-table th {
    background: #1E3A8A;
    color: white;
    padding: 12px;
    text-align: left;
}
.cost-table td {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}
.tip-box {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
</style>

<div class="life-header">
    <h1 style="color: white; font-size: 36px;">🎓 Student Life in Asia: Complete Guide</h1>
    <p style="font-size: 18px;">Discover What It's Really Like to Study in China, Singapore, Malaysia, Japan & Korea</p>
</div>

<div class="life-stats">
    <div class="stat-card">
        <div class="stat-number">500K+</div>
        <div>International Students</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">190+</div>
        <div>Countries Represented</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">$300-1,200</div>
        <div>Monthly Living Cost</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div>Safety Rating</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">1000+</div>
        <div>Student Clubs</div>
    </div>
</div>

<div class="country-tab">
    <button class="tab-btn active" onclick="showCountry('china')">🇨🇳 China</button>
    <button class="tab-btn" onclick="showCountry('singapore')">🇸🇬 Singapore</button>
    <button class="tab-btn" onclick="showCountry('malaysia')">🇲🇾 Malaysia</button>
    <button class="tab-btn" onclick="showCountry('japan')">🇯🇵 Japan</button>
    <button class="tab-btn" onclick="showCountry('korea')">🇰🇷 Korea</button>
</div>

<!-- CHINA -->
<div id="china" class="country-card active">
    <div class="country-title">
        <span class="flag">🇨🇳</span>
        <h2>Student Life in China</h2>
    </div>
    
    <div class="life-grid">
        <div class="life-card">
            <h3>🏠 Accommodation</h3>
            <ul>
                <li><strong>University Dorms:</strong> ¥800-1,500/month</li>
                <li><strong>Private Apartment:</strong> ¥2,500-5,000/month</li>
                <li><strong>Share House:</strong> ¥1,500-3,000/month</li>
                <li>Most international students live on campus first year</li>
                <li>Modern facilities with 24/7 security</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🍜 Food & Cuisine</h3>
            <ul>
                <li><strong>University Cafeteria:</strong> ¥15-30/meal</li>
                <li><strong>Street Food:</strong> ¥10-20</li>
                <li><strong>Restaurant:</strong> ¥30-80/meal</li>
                <li>Famous dishes: Peking Duck, Xiaolongbao, Hot Pot</li>
                <li>Halal and vegetarian options available</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🚇 Transportation</h3>
            <ul>
                <li><strong>Subway/Metro:</strong> ¥3-8/trip</li>
                <li><strong>Bus:</strong> ¥1-3/trip</li>
                <li><strong>DiDi (Uber):</strong> ¥15-50/trip</li>
                <li><strong>Student Discount:</strong> 50% off public transport</li>
                <li>High-speed rail connects all major cities</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🎉 Festivals & Events</h3>
            <ul>
                <li><strong>Chinese New Year:</strong> Jan/Feb, 7-day holiday</li>
                <li><strong>Mid-Autumn Festival:</strong> Sep/Oct, mooncakes</li>
                <li><strong>Dragon Boat Festival:</strong> May/June, boat races</li>
                <li><strong>University Festival:</strong> Each university has annual cultural festival</li>
            </ul>
        </div>
    </div>
    
    <h3>💰 Monthly Budget Breakdown</h3>
    <table class="cost-table">
        <tr><th>Expense</th><th>Cost (CNY)</th><th>Cost (USD)</th></tr>
        <tr><td>Accommodation</td><td>800-1,500</td><td>$110-210</td></tr>
        <tr><td>Food</td><td>1,500-2,500</td><td>$210-350</td></tr>
        <tr><td>Transport</td><td>200-300</td><td>$28-42</td></tr>
        <tr><td>Utilities & Internet</td><td>300-500</td><td>$42-70</td></tr>
        <tr><td>Entertainment</td><td>500-1,000</td><td>$70-140</td></tr>
        <tr style="background:#D4AF37; font-weight:bold;"><td>TOTAL</td><td>3,300-5,800</td><td>$460-810</td></tr>
    </table>
    
    <div class="tip-box">
        <h3>💡 Pro Tips for China</h3>
        <ul>
            <li>Download WeChat and Alipay – essential for payments</li>
            <li>Learn basic Mandarin for daily interactions</li>
            <li>Join student clubs to make local friends</li>
            <li>Try street food – it's safe and delicious</li>
            <li>Travel during holidays to explore China's wonders</li>
        </ul>
    </div>
</div>

<!-- SINGAPORE -->
<div id="singapore" class="country-card">
    <div class="country-title">
        <span class="flag">🇸🇬</span>
        <h2>Student Life in Singapore</h2>
    </div>
    
    <div class="life-grid">
        <div class="life-card">
            <h3>🏠 Accommodation</h3>
            <ul>
                <li><strong>University Dorms:</strong> SGD 400-800/month</li>
                <li><strong>HDB Flat (shared):</strong> SGD 800-1,500/month</li>
                <li><strong>Condo (private):</strong> SGD 1,500-2,500/month</li>
                <li>Most students stay in dorms first year</li>
                <li>Air conditioning essential</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🍜 Food & Cuisine</h3>
            <ul>
                <li><strong>Hawker Center:</strong> SGD 3-6/meal</li>
                <li><strong>Food Court:</strong> SGD 5-8/meal</li>
                <li><strong>Restaurant:</strong> SGD 15-30/meal</li>
                <li>Famous dishes: Chicken Rice, Laksa, Chili Crab</li>
                <li>Halal, vegetarian, vegan options everywhere</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🚇 Transportation</h3>
            <ul>
                <li><strong>MRT/Bus:</strong> SGD 1.50-2.50/trip</li>
                <li><strong>Student Pass:</strong> SGD 50-100/month</li>
                <li><strong>Grab/Taxi:</strong> SGD 10-25/trip</li>
                <li>Excellent public transport system</li>
                <li>Singapore is very walkable</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🎉 Festivals & Events</h3>
            <ul>
                <li><strong>Chinese New Year:</strong> Jan/Feb, Chinatown celebrations</li>
                <li><strong>National Day:</strong> Aug 9, fireworks and parades</li>
                <li><strong>Singapore Grand Prix:</strong> Sep, Formula 1 night race</li>
                <li><strong>University festivals:</strong> Annual cultural shows</li>
            </ul>
        </div>
    </div>
    
    <h3>💰 Monthly Budget Breakdown</h3>
    <table class="cost-table">
        <tr><th>Expense</th><th>Cost (SGD)</th><th>Cost (USD)</th></tr>
        <tr><td>Accommodation</td><td>500-1,500</td><td>$375-1,125</td></tr>
        <tr><td>Food</td><td>400-600</td><td>$300-450</td></tr>
        <tr><td>Transport</td><td>100-150</td><td>$75-112</td></tr>
        <tr><td>Utilities & Internet</td><td>100-200</td><td>$75-150</td></tr>
        <tr><td>Entertainment</td><td>200-400</td><td>$150-300</td></tr>
        <tr style="background:#D4AF37; font-weight:bold;"><td>TOTAL</td><td>1,300-2,850</td><td>$975-2,137</td></tr>
    </table>
    
    <div class="tip-box">
        <h3>💡 Pro Tips for Singapore</h3>
        <ul>
            <li>Eat at hawker centers – affordable and authentic</li>
            <li>Use the MRT – fastest way to get around</li>
            <li>Join orientation week to make friends</li>
            <li>Respect local customs and rules</li>
            <li>Explore nearby countries on weekends (Malaysia, Indonesia)</li>
        </ul>
    </div>
</div>

<!-- MALAYSIA -->
<div id="malaysia" class="country-card">
    <div class="country-title">
        <span class="flag">🇲🇾</span>
        <h2>Student Life in Malaysia</h2>
    </div>
    
    <div class="life-grid">
        <div class="life-card">
            <h3>🏠 Accommodation</h3>
            <ul>
                <li><strong>University Dorms:</strong> RM 400-800/month</li>
                <li><strong>Private Apartment:</strong> RM 800-1,500/month</li>
                <li><strong>Shared House:</strong> RM 500-1,000/month</li>
                <li>Most universities have on-campus housing</li>
                <li>Affordable living costs</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🍜 Food & Cuisine</h3>
            <ul>
                <li><strong>Mamak Stalls:</strong> RM 5-10/meal</li>
                <li><strong>Hawker Center:</strong> RM 6-12/meal</li>
                <li><strong>Restaurant:</strong> RM 15-30/meal</li>
                <li>Malaysian, Chinese, Indian cuisines</li>
                <li>Food paradise with endless options</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🚇 Transportation</h3>
            <ul>
                <li><strong>Public Bus:</strong> RM 1-3/trip</li>
                <li><strong>LRT/MRT:</strong> RM 2-5/trip</li>
                <li><strong>Grab (Uber):</strong> RM 8-20/trip</li>
                <li><strong>Student Discount:</strong> 50% off public transport</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🎉 Festivals & Events</h3>
            <ul>
                <li><strong>Hari Raya:</strong> March/April, Muslim celebration</li>
                <li><strong>Chinese New Year:</strong> Jan/Feb, lion dances</li>
                <li><strong>Deepavali:</strong> Oct/Nov, Festival of Lights</li>
                <li><strong>Rainforest World Music Festival:</strong> July</li>
            </ul>
        </div>
    </div>
    
    <h3>💰 Monthly Budget Breakdown</h3>
    <table class="cost-table">
        <tr><th>Expense</th><th>Cost (RM)</th><th>Cost (USD)</th></tr>
        <tr><td>Accommodation</td><td>400-1,000</td><td>$85-210</td></tr>
        <tr><td>Food</td><td>600-900</td><td>$130-190</td></tr>
        <tr><td>Transport</td><td>100-150</td><td>$20-30</td></tr>
        <tr><td>Utilities & Internet</td><td>150-250</td><td>$30-50</td></tr>
        <tr><td>Entertainment</td><td>200-400</td><td>$40-85</td></tr>
        <tr style="background:#D4AF37; font-weight:bold;"><td>TOTAL</td><td>1,450-2,700</td><td>$305-565</td></tr>
    </table>
    
    <div class="tip-box">
        <h3>💡 Pro Tips for Malaysia</h3>
        <ul>
            <li>Explore diverse cuisines – Malay, Chinese, Indian</li>
            <li>Travel to Penang, Langkawi, and Borneo</li>
            <li>Learn basic Malay phrases</li>
            <li>Join cultural clubs to experience diversity</li>
            <li>Use Grab for affordable transport</li>
        </ul>
    </div>
</div>

<!-- JAPAN -->
<div id="japan" class="country-card">
    <div class="country-title">
        <span class="flag">🇯🇵</span>
        <h2>Student Life in Japan</h2>
    </div>
    
    <div class="life-grid">
        <div class="life-card">
            <h3>🏠 Accommodation</h3>
            <ul>
                <li><strong>University Dorms:</strong> ¥30,000-50,000/month</li>
                <li><strong>Share House:</strong> ¥50,000-70,000/month</li>
                <li><strong>Apartment (1K):</strong> ¥60,000-100,000/month</li>
                <li>Key money and deposit required</li>
                <li>Futon beds are common</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🍜 Food & Cuisine</h3>
            <ul>
                <li><strong>Convenience Store:</strong> ¥500-800/meal</li>
                <li><strong>Ramen Shop:</strong> ¥700-1,000</li>
                <li><strong>University Cafeteria:</strong> ¥300-500</li>
                <li>Famous: Sushi, Ramen, Tempura, Okonomiyaki</li>
                <li>7-Eleven, FamilyMart, Lawson everywhere</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🚇 Transportation</h3>
            <ul>
                <li><strong>Train/Subway:</strong> ¥200-500/trip</li>
                <li><strong>Student Commuter Pass:</strong> ¥5,000-10,000/month</li>
                <li><strong>Shinkansen:</strong> ¥13,000 (Tokyo-Osaka)</li>
                <li>Punctual and clean public transport</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🎉 Festivals & Events</h3>
            <ul>
                <li><strong>Sakura (Cherry Blossom):</strong> March-April</li>
                <li><strong>Gion Matsuri:</strong> July, Kyoto festival</li>
                <li><strong>Tanabata:</strong> July 7, Star Festival</li>
                <li><strong>Obon:</strong> August, ancestors festival</li>
            </ul>
        </div>
    </div>
    
    <h3>💰 Monthly Budget Breakdown</h3>
    <table class="cost-table">
        <tr><th>Expense</th><th>Cost (JPY)</th><th>Cost (USD)</th></tr>
        <tr><td>Accommodation</td><td>40,000-80,000</td><td>$270-540</td></tr>
        <tr><td>Food</td><td>30,000-50,000</td><td>$200-340</td></tr>
        <tr><td>Transport</td><td>10,000-15,000</td><td>$70-100</td></tr>
        <tr><td>Utilities</td><td>10,000-15,000</td><td>$70-100</td></tr>
        <tr><td>Entertainment</td><td>15,000-25,000</td><td>$100-170</td></tr>
        <tr style="background:#D4AF37; font-weight:bold;"><td>TOTAL</td><td>105,000-185,000</td><td>$710-1,250</td></tr>
    </table>
    
    <div class="tip-box">
        <h3>💡 Pro Tips for Japan</h3>
        <ul>
            <li>Learn basic Japanese (daily interactions)</li>
            <li>Join circle activities (clubs) at university</li>
            <li>Try convenience store food – surprisingly good!</li>
            <li>Use Suica or Pasmo cards for transport</li>
            <li>Respect quietness on trains and public spaces</li>
        </ul>
    </div>
</div>

<!-- KOREA -->
<div id="korea" class="country-card">
    <div class="country-title">
        <span class="flag">🇰🇷</span>
        <h2>Student Life in Korea</h2>
    </div>
    
    <div class="life-grid">
        <div class="life-card">
            <h3>🏠 Accommodation</h3>
            <ul>
                <li><strong>University Dorms:</strong> ₩300,000-500,000/month</li>
                <li><strong>Goshiwon (cheap room):</strong> ₩300,000-500,000</li>
                <li><strong>One-room apartment:</strong> ₩500,000-800,000</li>
                <li>Key deposit required (₩5,000,000-10,000,000)</li>
                <li>Many students live in dorms first year</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🍜 Food & Cuisine</h3>
            <ul>
                <li><strong>University Cafeteria:</strong> ₩4,000-6,000/meal</li>
                <li><strong>Street Food:</strong> ₩2,000-5,000</li>
                <li><strong>Korean BBQ:</strong> ₩15,000-25,000</li>
                <li>Famous: Kimchi, Bibimbap, Fried Chicken, Tteokbokki</li>
                <li>24-hour restaurants available</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🚇 Transportation</h3>
            <ul>
                <li><strong>Subway/Bus:</strong> ₩1,250-2,000/trip</li>
                <li><strong>Student Monthly Pass:</strong> ₩50,000-80,000</li>
                <li><strong>Taxi:</strong> ₩3,800-10,000/trip</li>
                <li>Excellent subway system in Seoul</li>
            </ul>
        </div>
        <div class="life-card">
            <h3>🎉 Festivals & Events</h3>
            <ul>
                <li><strong>Lunar New Year:</strong> Jan/Feb, Seollal</li>
                <li><strong>Cherry Blossom:</strong> April, Jinhae Festival</li>
                <li><strong>Busan International Film Festival:</strong> October</li>
                <li><strong>University festivals:</strong> May/September, Daedongje</li>
            </ul>
        </div>
    </div>
    
    <h3>💰 Monthly Budget Breakdown</h3>
    <table class="cost-table">
        <tr><th>Expense</th><th>Cost (KRW)</th><th>Cost (USD)</th></tr>
        <tr><td>Accommodation</td><td>400,000-700,000</td><td>$300-525</td></tr>
        <tr><td>Food</td><td>350,000-500,000</td><td>$260-375</td></tr>
        <tr><td>Transport</td><td>50,000-80,000</td><td>$38-60</td></tr>
        <tr><td>Utilities & Phone</td><td>100,000-150,000</td><td>$75-112</td></tr>
        <tr><td>Entertainment</td><td>150,000-250,000</td><td>$112-187</td></tr>
        <tr style="background:#D4AF37; font-weight:bold;"><td>TOTAL</td><td>1,050,000-1,680,000</td><td>$785-1,260</td></tr>
    </table>
    
    <div class="tip-box">
        <h3>💡 Pro Tips for Korea</h3>
        <ul>
            <li>Join MT (Membership Training) – university retreats</li>
            <li>Try noraebang (karaoke) with friends</li>
            <li>Use Naver Maps (better than Google Maps in Korea)</li>
            <li>Learn Hangul – easy to learn in a few hours</li>
            <li>Experience Korean BBQ and fried chicken culture</li>
        </ul>
    </div>
</div>

<div class="tip-box" style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; text-align: center; margin-top: 30px;">
    <h2 style="color: white;">🌏 Your Asian Adventure Awaits!</h2>
    <p style="font-size: 18px;">No matter which country you choose, studying in Asia offers unforgettable experiences, lifelong friendships, and amazing career opportunities!</p>
    <p><strong>Start your journey today! 🇨🇳🇸🇬🇲🇾🇯🇵🇰🇷</strong></p>
</div>

<script>
function showCountry(country) {
    // Hide all country cards
    document.querySelectorAll('.country-card').forEach(card => {
        card.classList.remove('active');
    });
    // Show selected country card
    document.getElementById(country).classList.add('active');
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}
</script>
'''

# Update Article 28 (Student Life)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 28", (student_life_content,))
print("✅ Updated Student Life article (ID 28)")

# ==================== ARTICLE 29 & 30: COMPLETE APPLICATION TIMELINE GUIDE ====================
timeline_content = '''
<style>
.guide-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2D4FA8 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
}
.guide-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: linear-gradient(135deg, #D4AF37, #F3D03E);
    color: #1E3A8A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.timeline-year {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin: 30px 0;
}
.timeline-block {
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #D4AF37;
}
.timeline-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}
.timeline-month {
    background: #1E3A8A;
    color: white;
    padding: 8px 20px;
    border-radius: 30px;
    font-weight: bold;
}
.country-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 15px;
    margin: 20px 0;
}
.country-deadline {
    background: #EFF6FF;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.country-deadline .flag {
    font-size: 24px;
}
.country-deadline .name {
    font-weight: bold;
    color: #1E3A8A;
}
.checklist {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 20px 0;
}
.checklist-item {
    background: #EFF6FF;
    padding: 12px 15px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.checklist-item:before {
    content: "☐";
    color: #D4AF37;
    font-weight: bold;
    font-size: 18px;
}
.tips-card {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
}
.deadline-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
.deadline-table th {
    background: #1E3A8A;
    color: white;
    padding: 12px;
    text-align: left;
}
.deadline-table td {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
}
</style>

<div class="guide-header">
    <h1 style="color: white; font-size: 36px;">📅 Complete Application Timeline for Asian Universities</h1>
    <p style="font-size: 18px;">Your Step-by-Step Guide to a Successful Study Abroad Application</p>
</div>

<div class="guide-stats">
    <div class="stat-card">
        <div class="stat-number">18</div>
        <div>Months Preparation</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">5-8</div>
        <div>Universities to Apply</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">3-6</div>
        <div>Scholarships to Apply</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">95%</div>
        <div>Success with Planning</div>
    </div>
</div>

<h2>📖 Table of Contents</h2>
<ul>
    <li>1. Overview: The Complete Timeline</li>
    <li>2. 18-24 Months Before: Research Phase</li>
    <li>3. 12-18 Months Before: Preparation Phase</li>
    <li>4. 9-12 Months Before: Application Phase</li>
    <li>5. 6-9 Months Before: Submission Phase</li>
    <li>6. 3-6 Months Before: Decision Phase</li>
    <li>7. 0-3 Months Before: Visa & Arrival Phase</li>
    <li>8. Country-Specific Deadlines</li>
    <li>9. Document Checklist</li>
    <li>10. Tips for Success</li>
    <li>11. Frequently Asked Questions</li>
</ul>

<h2>1. Overview: The Complete Timeline</h2>

<div class="timeline-year">
    <div class="timeline-block">
        <div class="timeline-header">
            <div class="timeline-month">24-18 Months Before</div>
            <strong>🔍 Research Phase</strong>
        </div>
        <ul>
            <li>Research universities and programs</li>
            <li>Check admission requirements</li>
            <li>Explore scholarship opportunities</li>
            <li>Start saving money</li>
            <li>Talk to alumni and current students</li>
        </ul>
    </div>
    
    <div class="timeline-block">
        <div class="timeline-header">
            <div class="timeline-month">18-12 Months Before</div>
            <strong>📚 Preparation Phase</strong>
        </div>
        <ul>
            <li>Take language tests (IELTS/TOEFL/HSK/TOPIK/JLPT)</li>
            <li>Prepare for entrance exams (SAT/GRE/GMAT/EJU)</li>
            <li>Maintain excellent grades</li>
            <li>Build extracurricular portfolio</li>
            <li>Research potential supervisors (for graduate programs)</li>
        </ul>
    </div>
    
    <div class="timeline-block">
        <div class="timeline-header">
            <div class="timeline-month">12-9 Months Before</div>
            <strong>📝 Application Preparation Phase</strong>
        </div>
        <ul>
            <li>Request recommendation letters (2-3)</li>
            <li>Write personal statement (first draft)</li>
            <li>Prepare research proposal (for graduate programs)</li>
            <li>Gather academic transcripts and certificates</li>
            <li>Create a list of target universities (5-8)</li>
        </ul>
    </div>
    
    <div class="timeline-block">
        <div class="timeline-header">
            <div class="timeline-month">9-6 Months Before</div>
            <strong>✍️ Application Submission Phase</strong>
        </div>
        <ul>
            <li>Finalize application documents</li>
            <li>Submit applications before deadlines</li>
            <li>Apply for scholarships (CSC, KGSP, MEXT, etc.)</li>
            <li>Take entrance exams (EJU, etc.)</li>
            <li>Prepare for interviews</li>
        </ul>
    </div>
    
    <div class="timeline-block">
        <div class="timeline-header">
            <div class="timeline-month">6-3 Months Before</div>
            <strong>🎉 Decision Phase</strong>
        </div>
        <ul>
            <li>Receive admission decisions</li>
            <li>Accept offer from chosen university</li>
            <li>Apply for scholarship results</li>
            <li>Start visa application process</li>
            <li>Arrange accommodation</li>
        </ul>
    </div>
    
    <div class="timeline-block">
        <div class="timeline-header">
            <div class="timeline-month">3-0 Months Before</div>
            <strong>✈️ Visa & Arrival Phase</strong>
        </div>
        <ul>
            <li>Complete visa application</li>
            <li>Receive visa and passport</li>
            <li>Book flights</li>
            <li>Pack luggage</li>
            <li>Attend pre-departure orientation</li>
            <li>Arrive and register at university</li>
        </ul>
    </div>
</div>

<h2>2. Country-Specific Application Deadlines</h2>

<div class="country-grid">
    <div class="country-deadline">
        <div class="flag">🇨🇳</div>
        <div class="name">China</div>
        <div><strong>Fall Intake:</strong> March-May</div>
        <div><strong>Spring Intake:</strong> Oct-Nov</div>
        <div><strong>CSC Scholarship:</strong> Jan-Mar</div>
    </div>
    <div class="country-deadline">
        <div class="flag">🇸🇬</div>
        <div class="name">Singapore</div>
        <div><strong>Fall Intake:</strong> Feb-Mar</div>
        <div><strong>Spring Intake:</strong> Aug-Sep</div>
        <div><strong>SINGA:</strong> Jun/Dec</div>
    </div>
    <div class="country-deadline">
        <div class="flag">🇲🇾</div>
        <div class="name">Malaysia</div>
        <div><strong>Fall Intake:</strong> May-Jun</div>
        <div><strong>Spring Intake:</strong> Nov-Dec</div>
        <div><strong>MIS:</strong> May</div>
    </div>
    <div class="country-deadline">
        <div class="flag">🇯🇵</div>
        <div class="name">Japan</div>
        <div><strong>Fall Intake:</strong> Jan-Feb</div>
        <div><strong>Spring Intake:</strong> Aug-Sep</div>
        <div><strong>MEXT:</strong> Apr-May</div>
    </div>
    <div class="country-deadline">
        <div class="flag">🇰🇷</div>
        <div class="name">Korea</div>
        <div><strong>Fall Intake:</strong> Apr-May</div>
        <div><strong>Spring Intake:</strong> Oct-Nov</div>
        <div><strong>KGSP:</strong> Feb-Mar</div>
    </div>
</div>

<h2>3. Detailed Country Timeline</h2>

<h3>🇨🇳 China</h3>
<table class="deadline-table">
    <tr><th>Month</th><th>Action</th></tr>
    <tr><td>January-March</td><td>CSC Scholarship application (Type A - Embassy Track)</td></tr>
    <tr style="background:#f5f5f5;"><td>February-April</td><td>CSC Scholarship (Type B - University Track), University applications</td></tr>
    <tr><td>March-May</td><td>Submit university applications for fall intake</td></tr>
    <tr style="background:#f5f5f5;"><td>May-June</td><td>University review, interview invitations</td></tr>
    <tr><td>July-August</td><td>Results announced, admission letters sent</td></tr>
    <tr style="background:#f5f5f5;"><td>August-September</td><td>Visa application, arrival in China</td></tr>
    <tr><td>September</td><td>Fall semester begins</td></tr>
</table>

<h3>🇸🇬 Singapore</h3>
<table class="deadline-table">
    <tr><th>Month</th><th>Action</th></tr>
    <tr><td>October-November</td><td>Start preparing application documents</td></tr>
    <tr style="background:#f5f5f5;"><td>December-January</td><td>Take IELTS/TOEFL, SAT if needed</td></tr>
    <tr><td>February-March</td><td>Submit applications (NUS, NTU, SMU)</td></tr>
    <tr style="background:#f5f5f5;"><td>March-April</td><td>Scholarship applications (ASEAN, NUS Merit)</td></tr>
    <tr><td>April-May</td><td>Interviews for shortlisted candidates</td></tr>
    <tr style="background:#f5f5f5;"><td>May-June</td><td>Admission results released</td></tr>
    <tr><td>July-August</td><td>Visa application, arrival</td></tr>
    <tr style="background:#f5f5f5;"><td>August</td><td>Fall semester begins</td></tr>
</table>

<h3>🇯🇵 Japan</h3>
<table class="deadline-table">
    <tr><th>Month</th><th>Action</th></tr>
    <tr><td>April-May</td><td>MEXT Scholarship (Embassy Track) application</td></tr>
    <tr style="background:#f5f5f5;"><td>June</td><td>EJU Examination (June session)</td></tr>
    <tr><td>July-August</td><td>University applications (fall intake)</td></tr>
    <tr style="background:#f5f5f5;"><td>September-October</td><td>University entrance exams, interviews</td></tr>
    <tr><td>November</td><td>EJU Examination (November session)</td></tr>
    <tr style="background:#f5f5f5;"><td>December-January</td><td>Admission results</td></tr>
    <tr><td>February-March</td><td>Visa application</td></tr>
    <tr style="background:#f5f5f5;"><td>April</td><td>Spring semester begins (main intake)</td></tr>
</table>

<h3>🇰🇷 Korea</h3>
<table class="deadline-table">
    <tr><th>Month</th><th>Action</th></tr>
    <tr><td>February-March</td><td>KGSP Scholarship (Embassy Track) application</td></tr>
    <tr style="background:#f5f5f5;"><td>March-April</td><td>KGSP (University Track), University applications</td></tr>
    <tr><td>April-May</td><td>University applications for fall intake</td></tr>
    <tr style="background:#f5f5f5;"><td>May-June</td><td>Interviews, document verification</td></tr>
    <tr><td>June-July</td><td>Admission results</td></tr>
    <tr style="background:#f5f5f5;"><td>July-August</td><td>Visa application</td></tr>
    <tr><td>September</td><td>Fall semester begins</td></tr>
</table>

<h2>4. Essential Document Checklist</h2>

<div class="checklist">
    <div class="checklist-item">Valid passport (6+ months validity)</div>
    <div class="checklist-item">Academic transcripts (notarized)</div>
    <div class="checklist-item">Degree certificates/diplomas</div>
    <div class="checklist-item">Language test scores (IELTS/TOEFL/HSK/TOPIK/JLPT)</div>
    <div class="checklist-item">Entrance exam scores (SAT/GRE/GMAT/EJU)</div>
    <div class="checklist-item">Personal statement (1,000-2,000 words)</div>
    <div class="checklist-item">Research proposal (for graduate programs)</div>
    <div class="checklist-item">2-3 recommendation letters</div>
    <div class="checklist-item">Curriculum Vitae (CV) / Resume</div>
    <div class="checklist-item">Portfolio (for arts/design programs)</div>
    <div class="checklist-item">Financial proof (bank statements)</div>
    <div class="checklist-item">Physical examination form</div>
    <div class="checklist-item">Passport photos (white background)</div>
    <div class="checklist-item">Scholarship application forms</div>
</div>

<h2>5. Tips for Success</h2>

<div class="tips-card">
    <h3>🎯 10 Essential Tips for a Successful Application</h3>
    <ol>
        <li><strong>Start Early:</strong> Begin 12-18 months before your intended start date</li>
        <li><strong>Research Thoroughly:</strong> Know each university's requirements and deadlines</li>
        <li><strong>Prepare Documents in Advance:</strong> Get transcripts and recommendation letters early</li>
        <li><strong>Write a Compelling Personal Statement:</strong> Tell YOUR unique story</li>
        <li><strong>Apply to Multiple Universities:</strong> 5-8 universities to increase chances</li>
        <li><strong>Apply for Multiple Scholarships:</strong> Don't rely on just one</li>
        <li><strong>Get Strong Recommendations:</strong> Ask professors who know you well</li>
        <li><strong>Prepare for Interviews:</strong> Practice common questions</li>
        <li><strong>Double-Check Everything:</strong> One mistake can delay your application</li>
        <li><strong>Stay Organized:</strong> Use a spreadsheet to track deadlines</li>
    </ol>
</div>

<div class="tips-card">
    <h3>💡 Common Mistakes to Avoid</h3>
    <ul>
        <li>❌ Missing application deadlines</li>
        <li>❌ Submitting incomplete documents</li>
        <li>❌ Using generic personal statements</li>
        <li>❌ Not proofreading applications</li>
        <li>❌ Applying to only one university</li>
        <li>❌ Ignoring scholarship opportunities</li>
        <li>❌ Last-minute language tests</li>
        <li>❌ Not following instructions carefully</li>
    </ul>
</div>

<h2>6. Frequently Asked Questions</h2>

<div class="tips-card">
    <h3>❓ When should I start preparing for language tests?</h3>
    <p>Start 12-18 months before. Take the test 6-9 months before deadlines to allow time for retakes if needed.</p>
    
    <h3>❓ How many universities should I apply to?</h3>
    <p>5-8 universities: 2-3 dream schools, 2-3 target schools, 2 safety schools.</p>
    
    <h3>❓ Can I apply to multiple scholarships?</h3>
    <p>Yes! Apply to all you're eligible for. You can only accept one, but it increases your chances.</p>
    
    <h3>❓ What if I miss the deadline?</h3>
    <p>Most universities have a second intake (spring). You can also apply for the next fall intake.</p>
    
    <h3>❓ How important are recommendation letters?</h3>
    <p>Very important! Get letters from professors who know you well and can speak to your abilities.</p>
    
    <h3>❓ Can I apply without language test scores?</h3>
    <p>Some universities offer conditional admission, but you'll need to pass the test before enrollment.</p>
</div>

<div class="tips-card" style="background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; text-align: center;">
    <h2 style="color: white;">🎓 Start Your Journey Today!</h2>
    <p style="font-size: 18px;">With proper planning and preparation, your dream of studying in Asia is within reach!</p>
    <p><strong>Follow this timeline and you'll be on your way to success! 🌏</strong></p>
</div>
'''

# Update Article 29 (Application Timeline Part 1)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 29", (timeline_content,))
print("✅ Updated Application Timeline article (ID 29)")

# Update Article 30 (Application Timeline Part 2)
c.execute("UPDATE blog_posts SET content = ? WHERE id = 30", (timeline_content,))
print("✅ Updated Application Timeline article (ID 30)")

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅ COMPLETE! ALL 5 articles updated with ultra-detailed content:")
print("   - Article 1: CHINA (Complete guide with 50+ universities, CSC, cities)")
print("   - Article 11: Malaysia (30+ universities, detailed guide)")
print("   - Article 14: Singapore (complete guide with NUS/NTU/SMU details)")
print("   - Article 16: Japan (Universities, MEXT, EJU, JLPT)")
print("   - Article 17: Korea (Universities, KGSP, TOPIK, visa)")
print("="*60)
print("\nNow run: python app.py")
print("Then visit:")
print("   http://localhost:5000/article/1   (CHINA) 🇨🇳")
print("   http://localhost:5000/article/11  (Malaysia)")
print("   http://localhost:5000/article/14  (Singapore)")
print("   http://localhost:5000/article/16  (Japan)")
print("   http://localhost:5000/article/17  (Korea)")
