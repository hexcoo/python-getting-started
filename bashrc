cat << EOF
Welcome to your development container. Happy coding!
EOF
alias ll='ls -al'
ln -s /var/spool/cron/crontabs crontab
export PS1="\[\e[36m\]\${OKTETO_NAMESPACE:-okteto}:\[\e[32m\]\${OKTETO_NAME:-dev} \[\e[m\]\W> "
