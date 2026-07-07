#!/bin/bash
#======================================
# sprinterOS Bellatrix - Configuration Script
# Exo Computing (C) 2026
#======================================

# KIWI yardımcı fonksiyonlarını içeri al
source /etc/helper_functions.sh

# Herhangi bir hatada betiği durdur
set -e

echo "Build süreci başlıyor: sprinterOS Bellatrix..."

#--------------------------------------
# 1. Yerel Ayarlar ve Saat Dilimi
#--------------------------------------
baseConfig
baseSetupLocale
# İzmir/Türkiye yerel saat dilimini ayarla
ln -sf /usr/share/zoneinfo/Europe/Istanbul /etc/localtime

#--------------------------------------
# 2. Ağ Yapılandırması (DHCP)
#--------------------------------------
echo "Ağ yapılandırması (DHCP) hazırlanıyor..."

# Hostname ayarı
echo "exo25LC" > /etc/hostname

# Geleneksel Debian ağ yapılandırması (eth0 üzerinden DHCP)
cat > /etc/network/interfaces << EOF
auto lo
iface lo inet loopback

# Ana Ethernet arayüzü - DHCP aktif
auto eth0
allow-hotplug eth0
iface eth0 inet dhcp
EOF

# DNS Çözümleyicileri (Google & Cloudflare)
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 1.1.1.1" >> /etc/resolv.conf

#--------------------------------------
# 3. Markalama ve Görsel Kimlik (Branding)
#--------------------------------------
# os-release dosyasını kurumsal kimliğe uygun hale getir
cat > /etc/os-release << EOF
NAME="sprinterOS"
VERSION="Bellatrix"
ID=sprinteros
ID_LIKE=debian
VERSION_ID="1.42.1"
VERSION_CODENAME=bookworm
PRETTY_NAME="sprinterOS Bellatrix"
VENDOR_NAME="exo computing"
ANSI_COLOR="0;35"
HOME_URL="https://github.com/ygokbunar/sprinterOS"
SUPPORT_URL="mailto:ygokbunar@gmail.com"
LOGO=/etc/sprinteros-logo.png
EOF

# Profile göre logo seçimi (Classic vs AX_RX/RPI2)
#if [ "$kiwi_profiles" == "Classic" ]; then
    # 50 MHz model için minimalist core logo
    #cp /usr/share/pixmaps/sprinteros-core.png /etc/sprinteros-logo.png
#else
    # RPI ve üst modeller için özgün Frutiger Aero tasarımı
    #cp /usr/share/pixmaps/sprinteros-glossy.png /etc/sprinteros-logo.png
#fi

# IceWM temasını varsayılan olarak ata
#if [ -d /etc/X11/icewm ]; then
    # Senin exoclassic temanı varsayılan yapar
    #echo 'Theme="exoclassic/default.theme"' > /etc/X11/icewm/theme
#fi

if [ -f /etc/default/grub ]; then
    # GRUB menüsündeki dağıtım ismini değiştir
    sed -i 's/GRUB_DISTRIBUTOR=.*/GRUB_DISTRIBUTOR="sprinterOS Bellatrix"/' /etc/default/grub
    
    # İsteğe bağlı: Menüde "Advanced options for..." kısmını da özelleştirebilirsin
    # update-grub komutu KIWI'nin imaj paketleme aşamasında otomatik tetiklenir, 
    # ama dosyayı şimdiden hazırlamak markayı mühürler.
fi

#--------------------------------------
# 4. Kullanıcı Yönetimi
#--------------------------------------
# 'exo' kullanıcısını oluştur ve yetkilendir
if ! id "exo" &>/dev/null; then
    useradd -m -s /bin/bash exo
    echo "exo:1234" | chpasswd
    # GPIO, ses ve yönetim yetkilerini ver
    usermod -aG sudo,audio,video,gpio exo
fi

#--------------------------------------
# 5. Dosya İzinleri ve Servisler
#--------------------------------------
# LED Sequence betiğine çalışma izni ver
if [ -f /usr/bin/exocore-led-sequence.py ]; then
    chmod +x /usr/bin/exocore-led-sequence.py
fi

# Ağ servislerini etkinleştir
systemctl enable networking
if [ -f /usr/sbin/NetworkManager ]; then
    systemctl enable NetworkManager
fi

# Mac-usulü açılış sesi (Chime) servisi
if [ -f /etc/systemd/system/sprinteros-chime.service ]; then
    systemctl enable sprinteros-chime.service
fi

# Solar Sequence (4 Gezegen Işığı) LED Servisi
if [ -f /etc/systemd/system/exocore-led-daemon.service ]; then
    systemctl enable exocore-led-daemon.service
fi

# SSH Erişimi
if [ -f /lib/systemd/system/ssh.service ]; then
    systemctl enable ssh
fi

# Exo Office Kısayolları
if [ -d /etc/X11/icewm ]; then
    echo 'prog "AbiWord" abiword abiword' >> /etc/X11/icewm/menu
    echo 'prog "Gnumeric" gnumeric gnumeric' >> /etc/X11/icewm/menu
    echo 'prog "Chess" chess xboard' >> /etc/X11/icewm/menu
    echo 'prog "Badwolf" badwolf badwolf' >> /etc/X11/icewm/menu
fi



#--------------------------------------
# 6. Temizlik ve Optimizasyon
#--------------------------------------
apt-get clean
rm -rf /var/lib/apt/lists/*

# KIWI temizlik fonksiyonu
baseClean

echo "Build süreci tamamlandı. sprinterOS Bellatrix paketlenmeye hazır."
exit 0