# Homework 1 Report: Sledopyt

## Screenshot

Add a screenshot from Bash/WSL terminal where the result of this command is visible:

```bash
tree ~/secure_project
```

## evidence.log

```text
/home/xrtp/secure_project/backup/secret_plan_v1.txt:The password is 12345
```

## report.txt

```text
/home/xrtp/secure_project
├── backup
│   └── secret_plan_v1.txt
├── docs
│   └── secret_plan.txt
├── evidence.log
├── history.txt
├── report.txt
├── report_lesson1.md
└── src

3 directories, 6 files
```

## Command History

```text
  1  mkdir -p ~/secure_project/{docs,src,backup}
  2  printf 'The password is 12345\n' > ~/secure_project/docs/secret_plan.txt
  3  cp ~/secure_project/docs/secret_plan.txt ~/secure_project/backup/secret_plan_v1.txt
  4  grep -R 'password' ~/secure_project/backup > ~/secure_project/evidence.log
  5  sudo apt-get update
  6  sudo apt-get install -y tree
  7  tree ~/secure_project > ~/secure_project/report.txt
  8  cat ~/secure_project/evidence.log
  9  history
```
