# 🌟 Contributing to DreamJobs

🎉 Whether you're fixing a bug, adding a feature, or enhancing documentation — **every contribution makes a difference**.  
We're thrilled to have you here! This guide will help you get started with contributing smoothly and effectively.

---

## ⚙️ Prerequisites

Ensure you have the following tools installed:

- [Python](https://www.python.org/downloads/) (v3.8+)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

---

## 🛠️ How to Contribute

### ⭐ 1. Star and Fork the Repository

- Show your support by starring this repo!
- Fork the repository using the "Fork" button on the top right.

### 🐛 2. Create or Claim an Issue

- Browse the [Issues](https://github.com/your-username/DreamJobs/issues) tab.
- If your idea/bug isn’t listed, create a new issue with a clear and descriptive title.
- Please wait for a maintainer to assign the issue to you before you start working.

### 📥 3. Clone Your Fork Locally

```bash
git clone https://github.com/<your-username>/DreamJobs.git
cd DreamJobs
```

---

### 🌱 4. Set Up the Project Locally

#### Create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # for Linux/macOS
env\Scripts\activate     # for Windows
```

#### Install dependencies:

```bash
pip install -r requirements.txt
```

#### Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Start the development server:

```bash
python manage.py runserver
```

> Visit the site at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🌐 5. Environment Variables

Create a `.env` file in the root directory and set up the following (if needed):

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
```

> ⚠️ **Do not commit your `.env` file.** It contains sensitive information.

---

### 🔧 6. Create a New Branch

```bash
git checkout -b feature/<your-branch-name>
```

---

### ✏️ 7. Make Your Changes

- Follow consistent and clean coding practices.
- Add helpful comments where needed.
- Test your changes locally before pushing.

---

### ✅ 8. Stage, Commit, and Push

```bash
git add .
git commit -m "Add: [feature description]"  # or Fix: [bug description]
git push origin feature/<your-branch-name>
```

---

### 🔁 9. Open a Pull Request (PR)

- Go to your fork on GitHub and click **"Compare & pull request"**.
- Fill out a meaningful PR title and description.
- Link the relevant issue (e.g., `Closes #5`) if applicable.
- Submit and wait for review.

---

## 📌 Project Tech Stack

| Purpose        | Technologies                    |
|----------------|---------------------------------|
| **Frontend**    | HTML, CSS, JavaScript, Bootstrap |
| **Backend**     | Python, Django                  |
| **Database**    | SQLite                          |
| **Deployment**  | Render                          |

---

### 🔄 Keeping Your Fork Updated

```bash
git remote add upstream https://github.com/<original-owner>/DreamJobs.git
git fetch upstream
git checkout main
git merge upstream/main
```

---

## 🙌 Thank You!

Your contribution helps job seekers and employers connect better.  
Let’s build **DreamJobs** into something amazing — **together!** 💼🌟

---

### 💬 Questions or Help?

If you get stuck or have questions, feel free to reach out to the maintainer:

📧 **Email**: nigamkhushi125@gmail.com  
🔗 **LinkedIn**: [Khushi Nigam](https://www.linkedin.com/in/khushinigam7)
