read -p "¿Deseas Configurar Git ahora? (s/n): " git_response

if [[ "$git_response" == "s" || "$git_response" == "S" ]]; then
    #Instanndo git
    echo "Instalando Git..."
    sudo apt-get install git -y
    # Configurar Git
    echo "Configurando Git..."
    read -p "Introduce tu nombre de usuario de Git: " git_username
    git config --global user.name "$git_username"
    read -p "Introduce tu correo electrónico de Git: " git_email
    git config --global user.email "$git_email"
    git config --global user.ui true
    git config --global init.defaultBranch main
    git config --global core.autocrlf
    git config --global core.autocrlf input
fi