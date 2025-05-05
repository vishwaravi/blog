---
title: "MySQL 8.4 Manual Installation on Arch Linux (Binary Package)"
date: 2025-05-04T12:00:00Z
draft: false
description: "Step-by-step guide to manually install MySQL 8.4 on Arch Linux using the official binary tarball."
tags:
  - MySQL
  - Arch Linux
  - Manual Installation
  - Binary Package
---

![Image Description](/images/arch_mysql.png)
##  MySql in Arch or other Distros :

MySQL provides prebuilt `.deb` packages for Debian and Ubuntu, which can be installed using the APT package manager.

If you're setting up a database on Arch Linux, you might notice something unexpected — MySQL isn't in the official repositories. Instead, you'll find **MariaDB**, a drop-in replacement. So, why does Arch provide MariaDB instead of MySQL? The answer lies in a mix of **open-source values, community trust, and long-term sustainability**.

#### Arch’s Philosophy and the Community Preference

Arch Linux is known for its **rolling-release model** and a strong emphasis on **simplicity and openness**. It avoids software with unclear or restrictive licenses whenever possible. Given that MariaDB is licensed under the **GNU General Public License (GPL)** and developed in the open, it aligns more closely with Arch's values than Oracle's MySQL.

## 📦 1. Download MySQL Binary

In such cases, you can install MySQL directly from the **generic binary tarball** provided by Oracle. This method gives you more control over the version and setup, making it ideal for custom or production environments. Below is a step-by-step guide to installing MySQL on Arch Linux using the official binary distribution.

Go to: [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)  
Choose the latest Linux Generic binary (e.g., `mysql-8.4.5-linux-glibc2.28-x86_64.tar.xz`).

```bash
cd ~/Downloads
tar -xvf mysql-8.4.5-linux-glibc2.28-x86_64.tar.xz
sudo mv mysql-8.4.5-linux-glibc2.28-x86_64 /usr/local/mysql
```

---

## 👤 2. Create MySQL User and Group

```bash
sudo groupadd mysql
sudo useradd -r -g mysql -s /bin/false mysql
```

---

## 🔧 3. Set Permissions

```bash
cd /usr/local/mysql
sudo mkdir mysql-files
sudo chown -R mysql:mysql .
sudo chmod 750 mysql-files
```

---

## 🛠️ 4. Initialize MySQL Data Directory

```bash
sudo ./bin/mysqld --initialize --user=mysql
```

🔐 **Important:** This will output a **temporary root password**, like:

```
A temporary password is generated for root@localhost: aB1cDe2FgH!
```

➡️ **Note it down**, you'll need it to log in for the first time.

---

## ⚙️ 5. Create a MySQL Configuration File

```bash
sudo nano /usr/local/mysql/my.cnf
```

Paste:

```ini
[mysqld]
basedir=/usr/local/mysql
datadir=/usr/local/mysql/data
socket=/tmp/mysql.sock
pid-file=/usr/local/mysql/data/mysqld.pid
user=mysql
```

---

## ⚙️ 6. Create systemd Service

```bash
sudo nano /etc/systemd/system/mysql.service
```

Paste:

```ini
[Unit]
Description=MySQL Community Server
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/mysql/bin/mysqld_safe --defaults-file=/usr/local/mysql/my.cnf
ExecStop=/usr/local/mysql/bin/mysqladmin shutdown
User=mysql
Group=mysql
TimeoutSec=600
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## 🔄 7. Enable and Start MySQL

```bash
sudo systemctl daemon-reload
sudo systemctl enable mysql
sudo systemctl start mysql
```

---

## 🔍 8. Verify MySQL Is Running

```bash
sudo systemctl status mysql
```

Expected output: `active (running)`

---

## 🔐 9. Log In with Temporary Password and Set New Root Password

```bash
/usr/local/mysql/bin/mysql -u root -p
```

🔑 Enter the **temporary password** from step 4.

Then run:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_secure_password';
```

✅ Now you have full access with your new password.

---

## 🛡️ 10. Optional: Run Secure Installation Script

```bash
sudo /usr/local/mysql/bin/mysql_secure_installation
```

This will:
- Remove anonymous users
- Disallow remote root login
- Remove test database
- Reload privilege tables

---

## 🧠 Tip: Add MySQL to Your PATH

To avoid typing full paths every time:

```bash
echo 'export PATH=/usr/local/mysql/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```