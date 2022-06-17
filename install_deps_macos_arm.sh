
export LOCAL_PATH="${HOME}/.local"

brew install autoconf automake libtool


function install_proto(){
    # check if already install ros
    protoc --version
    ret=$?
    if [ $ret -eq 0 ];then
       echo "Protobuf is already installed, skip installing protobuf!"
       return 0
    fi

    # install protobuf
    export PROTO_PATH="${LOCAL_PATH}/opt/protobuf"
    git clone -b v3.19.1 --depth=1 --recurse-submodules --shallow-submodules -- https://github.com/protocolbuffers/protobuf ${PROTO_PATH} && cd ${PROTO_PATH} && ./autogen.sh && ./configure --prefix=${PROTO_PATH} && make -j2 && make install && mkdir -p ${LOCAL_PATH}/bin && ln -s ${PROTO_PATH}/bin/* ${LOCAL_PATH}/bin/
    echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.zshrc && . ~/.zshrc
    echo 'export PKG_CONFIG_PATH="${HOME}/.local/opt/protobuf/lib/pkgconfig:${PKG_CONFIG_PATH}"' >> ~/.zshrc && . ~/.zshrc

}

function install_poetry(){
    # check if already install ros
    poetry --version
    ret=$?
    if [ $ret -eq 0 ];then
       echo "Poetry is already installed, skip installing poetry!"
       return 0
    fi

    # install poetry
    export PROTO_PATH="${LOCAL_PATH}/opt/protobuf"
    curl -sSL https://install.python-poetry.org | python3.10 -

}

function install_anyenv(){
    # check if already install ros
    anyenv --version
    ret=$?
    if [ $ret -eq 0 ];then
       echo "Anyenv is already installed, skip installing anyenv!"
       return 0
    fi

    # install anyenv
    gh repo clone anyenv/anyenv ~/.local/opt/anyenv
    echo 'export ANYENV_ROOT="${HOME}/.local/opt/anyenv"
if [ -d $ANYENV_ROOT ]; then
  export PATH="${ANYENV_ROOT}/bin:${PATH}"
  eval "$(anyenv init -)"
  test -e "${PYENV_ROOT}/plugins/pyenv-virtualenv" && eval "$(pyenv virtualenv-init -)"
fi' >> ~/.zshrc

     anyenv install --init https://github.com/anyenv/anyenv-install.git

     anyenv install -l
}

function install_pyenv(){
    # check if already install ros
    pyenv --version
    ret=$?
    if [ $ret -eq 0 ];then
       echo "pyenv is already installed, skip installing pyenv!"
       return 0
    fi

    # install pyenv
    brew install openssl@1.1 readline
    anyenv install pyenv
    pyenv install 3.10.5 && pyenv rehash

}

function install_poetry(){
    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    pyenv shell 3.10.5

    # check if already install ros
    poetry --version
    ret=$?
    if [ $ret -eq 0 ];then
       echo "Poetry is already installed, skip installing poetry!"
       return 0
    fi

    # install poetry
    curl -sSL https://install.python-poetry.org | python3.10 -
}

function install_racoonai_deps(){
    poetry install

    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    pyenv shell --unset && poetry shell
    pre-commit install
}

install_racoonai_deps
