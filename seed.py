from app import app, db, Opportunity
from datetime import datetime, timedelta

opportunities_data = [
    {
        "title": "Python Developer Intern",
        "company": "Bincom Dev Center",
        "type": "internship",
        "location": "Lagos",
        "description": "Join our team as a Python Developer Intern. You will work on real projects, learn from senior developers, and contribute to production code. Great opportunity for students and fresh graduates.",
        "skills_required": "Python, HTML, CSS, Git",
        "deadline": datetime.now() + timedelta(days=30),
        "apply_link": "https://bincom.net/careers"
    },
    {
        "title": "Frontend Developer",
        "company": "Flutterwave",
        "type": "job",
        "location": "Lagos (Remote)",
        "description": "We are looking for a skilled Frontend Developer to build beautiful, responsive web interfaces. You will work with React, TypeScript, and modern CSS frameworks.",
        "skills_required": "JavaScript, React, CSS, HTML, TypeScript",
        "deadline": datetime.now() + timedelta(days=45),
        "apply_link": "https://flutterwave.com/careers"
    },
    {
        "title": "AI/ML Hackathon 2026",
        "company": "Google Nigeria",
        "type": "hackathon",
        "location": "Lagos",
        "description": "48-hour hackathon focused on AI and Machine Learning solutions for African problems. Prizes include internships, cash awards, and mentorship from Google engineers.",
        "skills_required": "Python, Machine Learning, TensorFlow, Data Analysis",
        "deadline": datetime.now() + timedelta(days=14),
        "apply_link": "https://events.google.com/hackathon"
    },
    {
        "title": "Web Development Intern",
        "company": "Enchanted Digital Academy",
        "type": "internship",
        "location": "Remote",
        "description": "Build landing pages, integrate forms, and learn modern web development practices. Work with HTML, CSS, JavaScript, and Python. Certificate and recommendation letter provided.",
        "skills_required": "HTML, CSS, JavaScript, Python, GitHub",
        "deadline": datetime.now() + timedelta(days=20),
        "apply_link": "https://enchanteddigitalacademy.com.ng/apply"
    },
    {
        "title": "Full Stack Developer",
        "company": "Paystack",
        "type": "job",
        "location": "Lagos",
        "description": "Join Paystack engineering team. Build and maintain payment infrastructure used by thousands of African businesses. Work with Node.js, PostgreSQL, and AWS.",
        "skills_required": "Node.js, PostgreSQL, AWS, JavaScript, API Design",
        "deadline": datetime.now() + timedelta(days=60),
        "apply_link": "https://paystack.com/careers"
    },
    {
        "title": "Data Science Intern",
        "company": "Andela Nigeria",
        "type": "internship",
        "location": "Lagos",
        "description": "Learn data science fundamentals and work on real datasets. You will use Python, pandas, scikit-learn, and visualization tools to extract insights.",
        "skills_required": "Python, pandas, SQL, Data Visualization, Statistics",
        "deadline": datetime.now() + timedelta(days=25),
        "apply_link": "https://andela.com/careers"
    },
    {
        "title": "Mobile App Developer",
        "company": "OPay",
        "type": "job",
        "location": "Lagos",
        "description": "Build mobile applications for one of Nigeria's leading fintech companies. Work with Flutter or React Native to create seamless user experiences.",
        "skills_required": "Flutter, Dart, React Native, Mobile Development, API Integration",
        "deadline": datetime.now() + timedelta(days=40),
        "apply_link": "https://opay.com/careers"
    },
    {
        "title": "Cybersecurity Challenge",
        "company": "Microsoft Nigeria",
        "type": "hackathon",
        "location": "Abuja",
        "description": "Test your cybersecurity skills in this 24-hour capture-the-flag competition. Learn from Microsoft security experts and win amazing prizes.",
        "skills_required": "Cybersecurity, Networking, Python, Linux, Ethical Hacking",
        "deadline": datetime.now() + timedelta(days=10),
        "apply_link": "https://microsoft.com/nigeria/events"
    },
    {
        "title": "UI/UX Design Intern",
        "company": "Kuda Bank",
        "type": "internship",
        "location": "Lagos (Hybrid)",
        "description": "Design user interfaces for mobile and web banking applications. Learn Figma, design systems, and user research methodologies.",
        "skills_required": "Figma, UI Design, UX Research, Prototyping, Adobe XD",
        "deadline": datetime.now() + timedelta(days=35),
        "apply_link": "https://kuda.com/careers"
    },
    {
        "title": "DevOps Engineer",
        "company": "Interswitch",
        "type": "job",
        "location": "Lagos",
        "description": "Manage cloud infrastructure, CI/CD pipelines, and deployment automation. Work with Docker, Kubernetes, and AWS to scale payment systems.",
        "skills_required": "Docker, Kubernetes, AWS, CI/CD, Linux, Python",
        "deadline": datetime.now() + timedelta(days=50),
        "apply_link": "https://interswitchgroup.com/careers"
    },
    {
        "title": "Blockchain Developer Intern",
        "company": "Bundle Africa",
        "type": "internship",
        "location": "Remote",
        "description": "Explore blockchain development and smart contracts. Work with Solidity, Web3.js, and Ethereum-based applications in the African crypto space.",
        "skills_required": "Solidity, Web3.js, JavaScript, Blockchain, Smart Contracts",
        "deadline": datetime.now() + timedelta(days=28),
        "apply_link": "https://bundle.africa/careers"
    },
    {
        "title": "Tech Startup Pitch Competition",
        "company": "Techstars Lagos",
        "type": "hackathon",
        "location": "Lagos",
        "description": "Pitch your tech startup idea to investors and mentors. Win funding, mentorship, and access to Techstars global network. Open to students and entrepreneurs.",
        "skills_required": "Entrepreneurship, Pitching, Business Development, Tech Knowledge",
        "deadline": datetime.now() + timedelta(days=21),
        "apply_link": "https://techstars.com/lagos"
    }
]

with app.app_context():
    Opportunity.query.delete()
    db.session.commit()
    for data in opportunities_data:
        opp = Opportunity(**data)
        db.session.add(opp)
    db.session.commit()
    print("Added " + str(len(opportunities_data)) + " sample opportunities!")
    print("\nOpportunities include:")
    for opp in opportunities_data:
        print("  - " + opp['title'] + " at " + opp['company'] + " (" + opp['type'] + ")")