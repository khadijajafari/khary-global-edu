// universities.js - University display and application functions
// University data loaded from server (this will be replaced by Flask variables)
const universityData = {
    china: [],
    singapore: [],
    malaysia: [],
    japan: [],
    korea: []
};

function showCountryUniversities(country, countryName) {
    const universities = universityData[country];
    if (!universities || universities.length === 0) {
        alert('No universities found for ' + countryName);
        return;
    }
    
    // Clear the page
    document.body.innerHTML = '';
    
    // Create header
    let html = '<div class="university-header">' +
        '<div class="container">' +
        '<div class="flag">' + countryName.split(' ')[0] + '</div>' +
        '<h1>Study in ' + countryName.split(' ')[1] + '</h1>' +
        '<p>' + universities.length + ' Top Universities • Complete Programs • Scholarship Opportunities</p>' +
        '</div></div>';
    
    // Add to body
    document.body.innerHTML = html;
    
    // Create container
    let containerHtml = '<div class="container">' +
        '<button class="back-button" onclick="location.reload()">← Back to Home</button>' +
        '<div class="university-grid">';
    
    // Add universities
    for(let i = 0; i < universities.length; i++) {
        let uni = universities[i];
        containerHtml += '<div class="university-card">' +
            '<div class="university-card-header">' +
            '<h3>' + uni.name + '</h3>' +
            '<div class="ranking">' + uni.ranking + '</div>' +
            '</div>' +
            '<div class="university-card-body">' +
            '<div class="info-item"><strong>📍 Location:</strong> ' + uni.location + '</div>' +
            '<div class="info-item"><strong>📅 Established:</strong> ' + uni.established + '</div>' +
            '<div class="info-item"><strong>👥 Students:</strong> ' + uni.students + '</div>' +
            '<p><em>' + uni.description + '</em></p>' +
            '<div class="program-section"><h4>📚 Undergraduate Programs</h4>';
        
        // Add undergraduate programs
        if (uni.programs && uni.programs.undergraduate) {
            for(let j = 0; j < uni.programs.undergraduate.length; j++) {
                containerHtml += '<span class="program-tag">' + uni.programs.undergraduate[j] + '</span>';
            }
        }
        
        containerHtml += '</div><div class="program-section"><h4>🎓 Graduate Programs</h4>';
        
        // Add graduate programs
        if (uni.programs && uni.programs.graduate) {
            for(let j = 0; j < uni.programs.graduate.length; j++) {
                containerHtml += '<span class="program-tag">' + uni.programs.graduate[j] + '</span>';
            }
        }
        
        containerHtml += '</div><div class="info-item"><strong>💰 Tuition:</strong> ' + uni.fees.undergraduate + '</div>';
        
        // Add scholarships
        if (uni.scholarships && uni.scholarships.length > 0) {
            containerHtml += '<div class="program-section"><h4>✨ Scholarships</h4>';
            for(let j = 0; j < Math.min(uni.scholarships.length, 3); j++) {
                let s = uni.scholarships[j];
                containerHtml += '<div class="scholarship-item">🏆 ' + s.name + ' - ' + s.coverage + '</div>';
            }
            containerHtml += '</div>';
        }
        
        containerHtml += '<button class="btn" onclick="showApplication(\'' + uni.name.replace(/'/g, "\\'") + '\', \'' + countryName.split(' ')[1] + '\')">Apply Now</button>' +
            '</div></div>';
    }
    
    containerHtml += '</div></div>';
    
    // Add to body
    document.body.innerHTML += containerHtml;
    
    // Add footer
    let footerHtml = '<footer class="footer">' +
        '<div class="container">' +
        '<p>© 2024 KHARY GLOBAL EDU. All rights reserved.</p>' +
        '<p>Study Abroad Guidance for Asian Universities</p>' +
        '</div></footer>';
    
    document.body.innerHTML += footerHtml;
}

function showApplication(university, country) {
    let modalHtml = '<div class="modal">' +
        '<div class="modal-content">' +
        '<h2>Apply to ' + university + '</h2>' +
        '<form id="applicationForm" enctype="multipart/form-data">' +
        '<label>Full Name *</label>' +
        '<input type="text" id="name" required>' +
        '<label>Email *</label>' +
        '<input type="email" id="email" required>' +
        '<label>Phone/WhatsApp *</label>' +
        '<input type="tel" id="phone" required>' +
        '<label>Program Level *</label>' +
        '<select id="program_level" required>' +
        '<option value="Undergraduate">Undergraduate</option>' +
        '<option value="Graduate">Graduate</option>' +
        '<option value="PhD">PhD</option>' +
        '<option value="Language">Language Course</option>' +
        '</select>' +
        '<label>Preferred Program</label>' +
        '<input type="text" id="preferred_program">' +
        '<label>📎 Upload Documents (PDF, DOC, JPG)</label>' +
        '<input type="file" id="documents" name="documents" multiple accept=".pdf,.doc,.docx,.jpg,.jpeg,.png" style="padding: 10px; border: 2px dashed var(--primary-blue); width: 100%;">' +
        '<p style="font-size: 0.9rem; color: var(--primary-blue); margin-top: 5px; margin-bottom: 15px;">📎 You can select multiple files (hold Ctrl/Cmd to select multiple)</p>' +
        '<label>Message/Questions</label>' +
        '<textarea id="message" rows="3"></textarea>' +
        '<div class="modal-buttons">' +
        '<button type="button" class="btn" onclick="submitApplication(\'' + university.replace(/'/g, "\\'") + '\', \'' + country + '\')">Submit Application</button>' +
        '<button type="button" class="btn" onclick="this.closest(\'.modal\').remove()" style="background:#ccc;">Close</button>' +
        '</div>' +
        '</form>' +
        '</div>' +
        '</div>';
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function submitApplication(university, country) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('university', university);
    formData.append('country', country);
    formData.append('student_name', document.getElementById('name').value);
    formData.append('student_email', document.getElementById('email').value);
    formData.append('student_phone', document.getElementById('phone').value);
    formData.append('program_level', document.getElementById('program_level').value);
    formData.append('preferred_program', document.getElementById('preferred_program').value);
    formData.append('message', document.getElementById('message').value);
    
    const files = document.getElementById('documents').files;
    for (let i = 0; i < files.length; i++) {
        formData.append('documents', files[i]);
    }
    
    fetch('/submit-application-with-files', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Thank you for applying to ' + university + '! We will contact you within 24 hours.');
            document.querySelector('.modal').remove();
        } else {
            alert('❌ Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('❌ Network error. Please try again.');
    });
}