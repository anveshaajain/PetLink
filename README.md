````markdown
# 🐾 PetLink - Pet Adoption and Management System

PetLink is a modern, full-stack Pet Adoption and Management System built using Python Flask and SQLite. It connects loving families with pets in need of homes through an intuitive and responsive web platform.

GitHub Repository: [https://github.com/anveshaajain/PetLink.git](https://github.com/anveshaajain/PetLink.git)

---

## ✨ Key Features

### 👤 For Pet Adopters
- **User Registration & Login:** Secure account creation with personal details.  
- **Profile Management:** Track and manage your profile and adoption history.  
- **Pet Browsing:** Explore available pets with categories like Dogs, Cats, Birds, and Others.  
- **Adoption Requests:** Submit detailed requests with personal messages.  
- **Request Tracking:** Monitor the status of your adoption requests (Pending, Approved, Rejected).  

### 🏥 For Pet Owners/Admins
- **Owner Dashboard:** Full-featured interface to manage pets and adoption requests.  
- **Pet Management:** Add, edit, or remove pets with full details.  
- **Adoption Request Handling:** Review, approve, or reject requests.  
- **Status Updates:** Keep pet adoption statuses current.  
- **Analytics:** View statistics about pets and adoption activities.  

### 🎨 User Experience
- **Responsive Design:** Fully functional on desktops, tablets, and mobiles.  
- **Dark/Light Mode:** Switch themes with preferences saved automatically.  
- **Modern Styling:** Clean, professional interface with smooth animations.  
- **Easy Navigation:** Intuitive and simple menu structure.  

### 📦 Database & Security
- **SQLite Database:** No external setup required.  
- **Preloaded Data:** Sample pets and categories included.  
- **Automatic Setup:** Database and tables created automatically on first run.  
- **Secure Storage:** Password hashing and safe data handling.  

---

## 🚀 Quick Start

1. **Clone the Project**
```bash
git clone https://github.com/anveshaajain/PetLink.git
cd PetLink
````

2. **Install Dependencies**

```bash
pip install flask
```

3. **Run the Application**
   The main file is `app.py`:

```bash
python app.py
```

4. **Open in Browser**

* Main app: [http://localhost:5000](http://localhost:5000)
* Owner login: [http://localhost:5000/owner-login](http://localhost:5000/owner-login)

**Demo Owner/Admin Credentials:**

* Email: `admin@petlink.com`
* Password: `admin123`

---

## 📱 How to Use

### For Pet Adopters

1. **Register** – Fill in all required details to create an account.
2. **Browse Pets** – Explore pets by category and view their profiles.
3. **Adopt a Pet** – Click “Adopt Me,” write a personal message, and submit your request.
4. **Track Requests** – Check your profile for adoption request updates.

### For Pet Owners/Admins

1. **Login** – Access the dashboard via the owner login page.
2. **Add Pets** – Add new pets with complete information and photos.
3. **Manage Requests** – Review adoption requests and approve or reject them.
4. **Update Pet Status** – Keep pet availability and adoption statuses updated.

---

## 🗂 Project Structure

```
PetLink/
├── app_fixed.py             # Main running file of the project
├── petlink.db               # SQLite database (auto-created)
├── templates/               # HTML templates
│   ├── base.html            # Base template with styling
│   ├── index.html           # Home page
│   ├── login.html           # User login
│   ├── register.html        # User registration
│   ├── owner_login.html     # Owner login
│   ├── profile.html         # User profile
│   ├── adopt.html           # Pet browsing page
│   └── owner_dashboard.html # Owner management
└── README.md                # This file
```

---

## 🔧 Technical Details

* **Backend:** Flask, SQLite, session-based authentication with password hashing
* **Frontend:** HTML5, CSS3, JavaScript, responsive layout, Font Awesome icons
* **Database Schema:** Users, Owners, Categories, Pets, Adoption Requests

---

## 🔒 Security Features

* Password hashing (SHA-256)
* Session-based authentication
* SQL injection prevention with parameterized queries
* Input validation and sanitization

---

## 🚀 Future Improvements

* Email notifications for adoption requests
* Advanced search and filters
* Pet photo upload
* User profile editing
* Adoption contract generation
* Payment integration
* Mobile app version
* Social media integration
* Pet care tips and vet resources

---

## 🐛 Troubleshooting

* **Port Conflicts:** Change Flask port in `app.py`
* **Database Issues:** Delete `petlink.db` and restart
* **Module Not Found:** Ensure Flask is installed (`pip install flask`)

---

## 🤝 Contributing

Contributions are welcome! You can:

* Report bugs
* Suggest new features
* Improve documentation or UI
* Add new functionality


