Name     : tensorflow-addons
Version  : 0.11.2
Release  : 11
URL      : https://github.com/tensorflow/addons/archive/v0.11.2/tensorflow-addons-0.11.2.tar.gz
Source0  : https://github.com/tensorflow/addons/archive/v0.11.2/tensorflow-addons-0.11.2.tar.gz
Summary  : Useful extra functionality for TensorFlow 2.x maintained by SIG-addons
Group    : Development/Tools
License  : Apache-2.0
Requires : tensorflow
Requires : typeguard
BuildRequires : bazel
BuildRequires : pip
BuildRequires : python3-dev
BuildRequires : rsync
BuildRequires : setuptools
BuildRequires : tensorflow
BuildRequires : typeguard
BuildRequires : wheel

# SOURCES BEGIN
Source10 : https://storage.googleapis.com/mirror.tensorflow.org/github.com/NVlabs/cub/archive/1.8.0.zip
Source11 : https://mirror.bazel.build/github.com/bazelbuild/rules_cc/archive/8bd6cd75d03c01bb82561a96d9c1f9f7157b13d0.zip
Source12 : https://mirror.bazel.build/github.com/bazelbuild/rules_java/archive/7cf3cefd652008d0a64a419c34c13bdca6c8f178.zip
# SOURCES END

%define __strip /bin/true
%define debug_package %{nil}

%description
TensorFlow Addons is a repository of contributions that conform to
well-established API patterns, but implement new functionality not available in
core TensorFlow. TensorFlow natively supports a large number of operators,
layers, metrics, losses, and optimizers. However, in a fast moving field like
ML, there are many interesting new developments that cannot be integrated into
core TensorFlow (because their broad applicability is not yet clear, or it is
mostly used by a smaller subset of the community).

%prep
%setup -q -n addons-%{version}

InstallCacheBazel() {
  sha256=$(sha256sum $1 | cut -f1 -d" ")
  mkdir -p /var/tmp/cache/content_addressable/sha256/$sha256
  cp $1 /var/tmp/cache/content_addressable/sha256/$sha256/file
}

# CACHE BAZEL BEGIN
InstallCacheBazel %{SOURCE10}
InstallCacheBazel %{SOURCE11}
InstallCacheBazel %{SOURCE12}
# CACHE BAZEL END

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1485959355

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${buildroot}/usr/lib64:${buildroot}/usr/lib:${builddir}/usr/
export TF_HEADER_DIR=$(python -c "import sys; print(sys.path[-1])")/tensorflow/include
export TF_SHARED_LIBRARY_DIR=$(python -c "import sys; print(sys.path[-1])")/tensorflow
export TF_SHARED_LIBRARY_NAME=libtensorflow_framework.so.2
export TF_CXX11_ABI_FLAG=1
export TF_NEED_CUDA=0

bazel --output_base=/var/tmp/bazel build \
  --repository_cache=/var/tmp/cache \
  --verbose_failures \
  //:build_pip_pkg

bazel-bin/build_pip_pkg /var/tmp/artifacts

%install
export SOURCE_DATE_EPOCH=1485959355

pip3 install \
  --no-deps \
  --force-reinstall \
  --ignore-installed \
  --root \
  %{buildroot} /var/tmp/artifacts/tensorflow_addons-%{version}-cp38-cp38-linux_x86_64.whl

%files
%defattr(-,root,root,-)
/usr/lib/python3*/site-packages/tensorflow_addons*
/usr/lib/python3*/site-packages/_foo.cpython*so
