#!/bin/bash
BASE_DIR=`dirname $0`
if [ -h $0 ]; then
    LINK_ABS_PATH=`readlink $0`
    BASE_DIR=`dirname $LINK_ABS_PATH`
fi
TARGET_DIR="$BASE_DIR/target"
BUILD_DIR="$BASE_DIR/target/mussui/"
DIRS="api db monitor mussui portal services static sysadmin templates"

# Check for build path
if [ ! -d $BUILD_DIR ]; then
    mkdir -p $BUILD_DIR
fi

# Get Branch Name
BRANCH_NAME="`git branch | grep "\*" | cut -d" " -f 2`"

VERSION=0

copy_source_code() {
    echo "Copy Source Code to Build Path"
    for dir in $DIRS
    do
        cp -r ${BASE_DIR}/${dir} $BUILD_DIR
    done
    files="manage.py requirements runserver.sh service.py"
    for file in $files
    do
        cp -r ${BASE_DIR}/${file} $BUILD_DIR
    done
    mkdir -p ${BUILD_DIR}/log
}

clean_souce_code_pyc_files() {
    echo "Remove Old pyc files"
    for file in `find ${BUILD_DIR} -name "*.pyc"`
    do
        rm $file
    done
}


build_python_code() {
    echo "Build Python Code"
    for dir in $DIRS
    do
        for file in `find ${BUILD_DIR}${dir} -name "*.py"`
        do
            python -m py_compile $file
        done
    done
}

clean_source_code() {
    echo "Clean Python Source Code"
    for dir in $DIRS
    do
        for file in `find ${BUILD_DIR}${dir} -name "*.py"`
        do
            if [[ $file == *"migrations"* ]]; then
                continue
            fi
            rm $file
        done
    done
    rm ${BUILD_DIR}mussui/config.pyc
}

create_tarball() {
    echo "Create Tarball"
    cd $TARGET_DIR; tar zcf mussui.tar.gz mussui
}

process_build() {
    # Copy Source Code
    copy_source_code
    clean_souce_code_pyc_files
    # Build Python Code
    build_python_code
    # Clean Source Code
    clean_source_code
    # Create Tarball
    create_tarball
}

case $1 in
    build)
        process_build
        ;;
    clean)
        rm -rf $BUILD_DIR
        ;;
    help)
        echo "build.sh (build|clean|help)"
        ;;
    *)
        process_build
        ;;
esac
