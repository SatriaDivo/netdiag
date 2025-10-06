# 📝 Assignment Ideas

Creative and educational assignment ideas for instructors using the **Netdiag Network Diagnostics Toolkit** in their computer networking and cybersecurity courses.

## 🎯 Assignment Categories

### 📚 **Beginner Level** (Week 1-4)
- Basic connectivity testing
- DNS resolution fundamentals
- Port identification exercises
- Network documentation basics

### 🎓 **Intermediate Level** (Week 5-8)
- Performance analysis projects
- Security assessment basics
- Troubleshooting scenarios
- Campus network analysis

### 🚀 **Advanced Level** (Week 9-12)
- Comprehensive network audits
- Custom monitoring solutions
- Research projects
- Industry simulation exercises

---

## 📖 Assignment 1: Campus Network Map

**Duration**: 2 weeks  
**Level**: Beginner  
**Points**: 100

### Objective
Create a comprehensive map of the campus network infrastructure using network diagnostic tools.

### Requirements
Students must:
1. **Discover Campus Services** (25 points)
   ```python
   # Example starter code
   campus_domains = [
       "polinela.ac.id",
       "elearning.polinela.ac.id",
       "library.polinela.ac.id",
       "portal.polinela.ac.id"
   ]
   
   # Students complete the analysis
   for domain in campus_domains:
       # TODO: Perform DNS lookup
       # TODO: Test connectivity
       # TODO: Identify services
       pass
   ```

2. **Document Network Architecture** (25 points)
   - Create visual network diagram
   - List all discovered services
   - Document IP addresses and hostnames

3. **Analyze Connectivity Patterns** (25 points)
   - Measure latency to different services
   - Identify network segments
   - Document routing paths

4. **Present Findings** (25 points)
   - Written report (1000 words)
   - Network diagram
   - Recommendations for improvements

### Deliverables
- Network topology diagram
- Service inventory spreadsheet
- Technical report with findings
- Python script with all tests

### Grading Rubric
- **Excellent (A)**: Complete discovery, professional documentation, insightful analysis
- **Good (B)**: Most services found, good documentation, adequate analysis
- **Satisfactory (C)**: Basic discovery, minimal documentation, surface-level analysis
- **Needs Improvement (D/F)**: Incomplete work, poor documentation

---

## 🔍 Assignment 2: DNS Detective

**Duration**: 1 week  
**Level**: Beginner-Intermediate  
**Points**: 75

### Objective
Investigate DNS infrastructure and troubleshoot DNS-related issues using detective work approach.

### Scenario
```
🕵️ Mystery: Students report that "elearning.polinela.ac.id" 
sometimes loads slowly or fails to load entirely. 
Your mission: Investigate and solve the DNS mystery!
```

### Investigation Tasks

#### Phase 1: Evidence Gathering (30 points)
```python
def dns_investigation():
    """DNS investigation starter template."""
    
    target = "elearning.polinela.ac.id"
    
    # TODO: Students complete these investigations
    
    # 1. Basic DNS lookup
    print("🔍 Basic DNS Information:")
    # Students add DNS lookup code here
    
    # 2. Compare multiple DNS servers
    dns_servers = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    print("\n🔍 DNS Server Comparison:")
    # Students add comparison code here
    
    # 3. Check DNS record types
    record_types = ['A', 'AAAA', 'MX', 'NS', 'CNAME']
    print("\n🔍 DNS Record Analysis:")
    # Students add record analysis code here
    
    # 4. Performance testing
    print("\n🔍 Performance Investigation:")
    # Students add performance testing code here

# Students run and analyze results
dns_investigation()
```

#### Phase 2: Pattern Analysis (25 points)
- Identify inconsistencies between DNS servers
- Measure query response times over time
- Check for DNS caching effects
- Document any timeout or failure patterns

#### Phase 3: Solution Report (20 points)
Write a detective-style report including:
- **The Mystery**: Description of the problem
- **Evidence Found**: Data and observations
- **Analysis**: What the evidence reveals
- **Solution**: Recommended fixes
- **Prevention**: How to avoid similar issues

### Bonus Challenges (+10 points each)
1. **DNS Propagation Check**: Test DNS consistency across multiple global DNS servers
2. **Historical Analysis**: Compare current DNS performance with baseline measurements
3. **Alternative Solutions**: Propose backup DNS strategies

---

## 🛡️ Assignment 3: Campus Security Audit

**Duration**: 3 weeks  
**Level**: Intermediate-Advanced  
**Points**: 150

### Objective
Conduct a comprehensive but ethical security assessment of campus web services.

### ⚠️ Important Ethical Guidelines
```
🛡️ ETHICAL HACKING AGREEMENT

Before starting this assignment, students must:
✅ Only test authorized campus domains
✅ Use non-invasive scanning techniques
✅ Report findings responsibly
✅ Never attempt to exploit vulnerabilities
✅ Document all testing activities

Violation of these guidelines results in immediate assignment failure
and potential disciplinary action.
```

### Assessment Framework

#### Week 1: Information Gathering (50 points)
```python
def security_audit_phase1():
    """Phase 1: Passive information gathering."""
    
    authorized_targets = [
        "polinela.ac.id",
        "elearning.polinela.ac.id",
        "library.polinela.ac.id"
    ]
    
    for target in authorized_targets:
        print(f"\n🔍 Security Assessment: {target}")
        
        # TODO: Students implement these checks
        
        # 1. SSL/TLS Configuration
        print("1. SSL/TLS Analysis:")
        # Students add SSL analysis code
        
        # 2. HTTP Security Headers
        print("2. Security Headers Check:")
        # Students add headers analysis code
        
        # 3. Service Enumeration
        print("3. Service Discovery:")
        # Students add ethical port scanning code
        
        # 4. DNS Security Features
        print("4. DNS Security Check:")
        # Students add DNS security analysis code

security_audit_phase1()
```

#### Week 2: Vulnerability Assessment (50 points)
- Use automated tools to identify potential vulnerabilities
- Analyze SSL certificate configurations
- Check for common web application security headers
- Document any security misconfigurations

#### Week 3: Reporting and Recommendations (50 points)
- Executive summary for administrators
- Technical details for IT staff
- Prioritized recommendations
- Implementation timeline

### Expected Deliverables
1. **Security Assessment Report**
   - Executive summary (1 page)
   - Technical findings (5-10 pages)
   - Risk assessment matrix
   - Remediation roadmap

2. **Python Security Scanner**
   - Custom tool combining multiple Netdiag functions
   - Automated report generation
   - Ethical scanning safeguards

3. **Presentation**
   - 15-minute presentation to class
   - Demo of custom security tool
   - Q&A session

---

## 📊 Assignment 4: Network Performance Baseline

**Duration**: 4 weeks  
**Level**: Intermediate  
**Points**: 125

### Objective
Establish performance baselines for campus network services and create monitoring dashboard.

### Project Phases

#### Week 1: Measurement Framework (30 points)
Design and implement comprehensive performance testing:

```python
def performance_baseline_framework():
    """Performance measurement framework."""
    
    # Define test targets
    test_targets = {
        'Internal': ['polinela.ac.id', '192.168.1.1'],
        'External': ['google.com', '8.8.8.8'],
        'Educational': ['github.com', 'stackoverflow.com']
    }
    
    # Define test parameters
    test_parameters = {
        'ping_count': 20,
        'test_interval': 300,  # 5 minutes
        'test_duration': 7 * 24 * 60 * 60,  # 1 week
        'metrics': ['latency', 'jitter', 'packet_loss']
    }
    
    # TODO: Students implement comprehensive testing framework
    # Students should create functions for:
    # 1. Automated data collection
    # 2. Data storage and analysis
    # 3. Trend identification
    # 4. Anomaly detection
```

#### Week 2-3: Data Collection (40 points)
- Run continuous monitoring for one week
- Collect data at regular intervals
- Handle network interruptions gracefully
- Store data in structured format

#### Week 4: Analysis and Reporting (35 points)
- Statistical analysis of performance data
- Identify patterns and trends
- Create performance dashboard
- Generate recommendations

#### Bonus: Real-time Dashboard (+20 points)
Create web-based dashboard showing:
- Real-time network status
- Historical performance trends
- Alert notifications
- Performance comparisons

---

## 🌐 Assignment 5: Protocol Deep Dive

**Duration**: 2 weeks  
**Level**: Advanced  
**Points**: 100

### Objective
Choose one network protocol and create comprehensive educational materials about it.

### Available Protocols
Students choose one:
- **HTTP/HTTPS**: Web protocols and security
- **DNS**: Domain name resolution system
- **SMTP/POP3/IMAP**: Email protocols
- **SSH**: Secure remote access
- **FTP/SFTP**: File transfer protocols

### Research Requirements

#### Technical Analysis (40 points)
```python
def protocol_analysis_template():
    """Template for protocol deep dive analysis."""
    
    # Example: HTTP/HTTPS Analysis
    
    # 1. Protocol Basics
    print("📡 Protocol Fundamentals:")
    # Students research and document:
    # - OSI layer operation
    # - Default ports
    # - Message format
    # - Connection types
    
    # 2. Practical Testing
    print("🧪 Practical Protocol Testing:")
    # Students implement tests using Netdiag:
    # - Service detection
    # - Performance analysis
    # - Security assessment
    # - Version identification
    
    # 3. Security Analysis
    print("🔒 Security Considerations:")
    # Students analyze:
    # - Common vulnerabilities
    # - Security best practices
    # - Encryption options
    # - Authentication methods
    
    # 4. Real-world Examples
    print("🌍 Campus Implementation:")
    # Students analyze campus usage:
    # - How campus uses this protocol
    # - Performance characteristics
    # - Security implementation
    # - Improvement recommendations

protocol_analysis_template()
```

#### Educational Materials (35 points)
Create teaching materials including:
- Protocol explanation for beginners
- Hands-on exercises
- Common troubleshooting scenarios
- Security best practices

#### Demonstration (25 points)
- 20-minute class presentation
- Interactive protocol demonstration
- Q&A session with classmates
- Practical troubleshooting demo

---

## 🎯 Assignment 6: Industry Simulation

**Duration**: 4 weeks  
**Level**: Advanced  
**Points**: 200

### Objective
Simulate real-world network operations role-playing as IT professionals.

### Simulation Scenario
```
🏢 SCENARIO: TechCorp Indonesia

You are the Network Operations Team for TechCorp Indonesia, 
a technology company with 500 employees across 3 locations:
- Jakarta Headquarters (200 employees)
- Lampung Branch Office (150 employees) 
- Remote Workers (150 employees)

The company relies heavily on:
- Web-based applications
- Video conferencing
- File sharing systems
- Email communications
- Customer database access

Your mission: Ensure optimal network performance and security
```

### Team Roles (4-5 students per team)
1. **Network Administrator**: Infrastructure monitoring
2. **Security Analyst**: Threat detection and response
3. **Performance Engineer**: Optimization and troubleshooting
4. **Compliance Officer**: Documentation and standards
5. **Project Manager**: Coordination and reporting

### Weekly Challenges

#### Week 1: Infrastructure Assessment
**Challenge**: New office network setup
- Design network monitoring strategy
- Establish performance baselines
- Create security assessment plan
- Document current state

#### Week 2: Incident Response
**Challenge**: Users report slow internet access
- Investigate performance issues
- Identify bottlenecks
- Implement solutions
- Document incident resolution

#### Week 3: Security Incident
**Challenge**: Suspicious network activity detected
- Conduct security investigation
- Analyze logs and network data
- Implement security measures
- Prepare incident report

#### Week 4: Capacity Planning
**Challenge**: Company expanding to new location
- Analyze current network capacity
- Predict future requirements
- Design expansion plan
- Present recommendations to management

### Deliverables
1. **Daily Operations Log**
2. **Weekly Status Reports**
3. **Incident Response Documentation**
4. **Final Presentation to "Management"**
5. **Network Operations Playbook**

---

## 🔬 Assignment 7: Research Project

**Duration**: 6 weeks  
**Level**: Advanced  
**Points**: 175

### Objective
Conduct original research on a network-related topic and contribute to the field.

### Research Topics (Student Choice)
1. **Network Performance in Educational Institutions**
2. **DNS Security in Developing Countries**
3. **Campus Network Optimization Techniques**
4. **IoT Device Security Assessment Methods**
5. **Network Monitoring Automation**
6. **Student-proposed topic (requires approval)**

### Research Framework

#### Literature Review (25 points)
- Review 15+ academic papers
- Identify research gaps
- Develop research questions
- Create literature summary

#### Methodology Development (50 points)
```python
def research_methodology_example():
    """Example research methodology for network performance study."""
    
    # Research Question: "How does network performance vary 
    # across different campus locations during peak usage?"
    
    # Data Collection Framework
    measurement_plan = {
        'locations': ['Library', 'Computer Lab', 'Dormitory', 'Admin Building'],
        'time_periods': ['Morning', 'Afternoon', 'Evening', 'Night'],
        'metrics': ['latency', 'throughput', 'packet_loss', 'jitter'],
        'duration': '4 weeks',
        'sample_frequency': 'Every 5 minutes'
    }
    
    # TODO: Students implement comprehensive data collection
    # Students should develop:
    # 1. Automated data collection scripts
    # 2. Data validation procedures
    # 3. Statistical analysis methods
    # 4. Visualization techniques
```

#### Data Collection (50 points)
- Implement research methodology
- Collect substantial dataset
- Ensure data quality and integrity
- Handle unexpected issues

#### Analysis and Conclusions (50 points)
- Statistical analysis of results
- Interpretation of findings
- Discussion of implications
- Identification of future work

### Final Deliverables
1. **Research Paper** (15-20 pages, academic format)
2. **Data Analysis Code** (Well-documented Python scripts)
3. **Dataset** (Cleaned and annotated)
4. **Conference-Style Presentation** (20 minutes + Q&A)
5. **Poster Session** (Academic poster format)

---

## 📊 Assignment Assessment Framework

### General Grading Criteria

#### Technical Competency (40%)
- Correct use of networking tools and concepts
- Quality of data collection and analysis
- Problem-solving approach
- Code quality and documentation

#### Communication Skills (25%)
- Written report clarity and organization
- Presentation skills and engagement
- Visual aids and documentation quality
- Professional communication style

#### Critical Thinking (20%)
- Analysis depth and insight
- Connection to broader concepts
- Innovation and creativity
- Evidence-based conclusions

#### Professionalism (15%)
- Meeting deadlines and requirements
- Ethical conduct and responsibility
- Collaboration and teamwork
- Attention to detail

### Assignment Difficulty Scaling

#### Beginner Assignments
- Focus on tool usage and basic concepts
- Guided exercises with clear instructions
- Emphasis on following procedures correctly
- Success measured by completion and understanding

#### Intermediate Assignments
- Combine multiple concepts and tools
- Require some independent problem-solving
- Include analysis and interpretation components
- Success measured by quality of analysis

#### Advanced Assignments
- Open-ended problems requiring creativity
- Significant independent research component
- Professional-level deliverables expected
- Success measured by innovation and impact

---

## 🎓 Capstone Portfolio Project

**Duration**: Full Semester  
**Level**: Advanced  
**Points**: 300 (30% of final grade)

### Objective
Create a comprehensive portfolio demonstrating mastery of network diagnostics and analysis.

### Portfolio Components

#### 1. Technical Skills Demonstration (100 points)
- Complete all basic and intermediate assignments
- Demonstrate proficiency with all Netdiag functions
- Show progression from beginner to advanced concepts

#### 2. Original Research Contribution (100 points)
- Conduct independent research project
- Contribute new knowledge or tools to the field
- Present findings at student research symposium

#### 3. Professional Development (50 points)
- Create professional LinkedIn profile highlighting skills
- Write technical blog posts about networking topics
- Participate in networking professional communities

#### 4. Industry Preparation (50 points)
- Complete mock technical interviews
- Prepare industry-relevant case studies
- Demonstrate readiness for internships/employment

### Portfolio Presentation
- 45-minute comprehensive presentation
- Demonstration of technical skills
- Discussion of career goals and preparation
- Q&A with industry professionals

---

**Educational Innovation: 🎓 | Real-world Application: 💼 | Career Preparation: 🚀**