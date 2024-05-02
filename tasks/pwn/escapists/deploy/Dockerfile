# Builder stage
FROM debian:bookworm as builder

# Install debootstrap
RUN apt-get update && apt-get install -y debootstrap

# Create a new Debian chroot
RUN debootstrap --variant=minbase stable /chroot

# Runner stage
FROM debian:bookworm as runner

# Install necessary packages
RUN apt-get update && apt-get install -y cron openssh-server

# Copy the chroot from the builder stage
COPY --from=builder /chroot /box

RUN useradd -m -d /home/perun -s /bin/bash perun && echo 'perun:slav_prostrel' | chpasswd
RUN echo 'Match User perun' >> /etc/ssh/sshd_config && echo 'ChrootDirectory /box' >> /etc/ssh/sshd_config
RUN mkdir /var/run/sshd
RUN ssh-keygen -A
RUN chown -R perun:perun /box/*

RUN chroot /box /bin/bash -c "apt-get update && apt-get install -y fish"
RUN chroot /box /bin/bash -c "mv /usr/bin/fish /usr/sbin/ && chmod 6777 /usr/sbin/fish && rm -f /usr/bin/fish"
RUN chroot /box /bin/bash -c "mkdir /var/backup && chown root:root /var/backup && chmod 0700 /var/backup"
RUN chroot /box /bin/bash -c "echo 'tar -czf /chroot_backup.tar.gz -C /box /root' > /var/backup/backup.sh && echo 'echo \`date\` > /box/var/backup/lastbackup.log' >> /var/backup/backup.sh && chmod +x /var/backup/backup.sh"
RUN chroot /box /bin/bash -c "echo '/flag.txt' > /var/backup/LAST_KNOWN_FLAG_LOCATION"
RUN chroot /box /bin/bash -c "echo 'root:ToBeHonestItsNotEvenNeeded' | chpasswd"
RUN chroot /box /bin/bash -c "addgroup --gid 1000 user &&useradd -m -d /home/perun -s /bin/bash --uid 1000 --gid 1000 perun && echo 'perun:slav_prostrel' | chpasswd"

# Set up the cron job to backup /var/backup from the chroot
RUN echo "*/5 * * * * root /box/var/backup/backup.sh" > /etc/cron.d/backup_cron
RUN chmod 0644 /etc/cron.d/backup_cron

# Create the backup directory
RUN echo 'vrnctf{HYPERB0REA_H4S_ORB1TAL_CANN0NS}' > /flag.txt


# Start the SSH daemon inside the chroot and cron daemon outside the chroot
CMD /usr/sbin/sshd -D & cron -f