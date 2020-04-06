Name     : tensorflow-addons
Version  : 0.6.0
Release  : 6
URL      : https://github.com/tensorflow/addons/archive/v0.6.0.tar.gz
Source0  : https://github.com/tensorflow/addons/archive/v0.6.0.tar.gz

Source9 : https://storage.googleapis.com/mirror.tensorflow.org/github.com/NVlabs/cub/archive/1.8.0.zip
Source10 : https://mirror.bazel.build/github.com/bazelbuild/rules_cc/archive/0d5f3f2768c6ca2faca0079a997a97ce22997a0c.zip

%define __strip /bin/true
%define debug_package %{nil}

Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0

Patch1 : 0001-Remove-tensorflow-gpu-dependency.patch

BuildRequires : pip
BuildRequires : python3-dev
BuildRequires : setuptools
BuildRequires : wheel
BuildRequires : bazel
BuildRequires : tensorflow
BuildRequires : rsync

Requires: tensorflow


%description
TensorFlow Addons is a repository of contributions that conform to well-established API patterns,
but implement new functionality not available in core TensorFlow. TensorFlow natively supports a
large number of operators, layers, metrics, losses, and optimizers. However, in a fast moving
field like ML, there are many interesting new developments that cannot be integrated into core
TensorFlow (because their broad applicability is not yet clear, or it is mostly used by a
smaller subset of the community).

%prep
%setup -q  -n addons-0.6.0

%patch1 -p1

%build
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C
export SOURCE_DATE_EPOCH=1485959355
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${buildroot}/usr/lib64:${buildroot}/usr/lib:${builddir}/usr/
export TF_CXX11_ABI_FLAG=1
export TF_HEADER_DIR=`python -c "import sys; print(sys.path[-1])"`/tensorflow_core/include
export TF_SHARED_LIBRARY_DIR=`python -c "import sys; print(sys.path[-1])"`/tensorflow_core
export TF_SHARED_LIBRARY_NAME=libtensorflow_framework.so.2

InstallCache() {
	sha256=`sha256sum $1 | cut -f1 -d" "`
	mkdir -p /tmp/cache/content_addressable/sha256/$sha256/
	cp $1 /tmp/cache/content_addressable/sha256/$sha256/file
}

InstallCache %{SOURCE9}
InstallCache %{SOURCE10}

bazel --output_base=/tmp/bazel build --repository_cache=/tmp/cache build_pip_pkg
bazel-bin/build_pip_pkg /tmp/artifacts

%install
export SOURCE_DATE_EPOCH=1485959355

pip3 install --no-deps --force-reinstall --root %{buildroot} /tmp/artifacts/tensorflow_addons-0.6.0.dev0-cp38-cp38-linux_x86_64.whl

%files
%defattr(-,root,root,-)
/usr/lib/python3*/site-packages/tensorflow_addons*
/usr/lib/python3*/site-packages/_foo.cpython*so
