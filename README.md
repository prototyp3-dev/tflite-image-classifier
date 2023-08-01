# Image Classifier DApp

This DApp receives an image as input and returns, in a notice, the 5 most probable classes according to a classifier based on the ImageNet dataset.

The goal of this app is to demonstrate the following features:
- Using TensorFlow Lite inside Cartesi Machine
- Build process using an external repository for addidtional python packages, containing precompiled RISC-V packages for numpy and Tensorflow Lite
- Organization of a Python DApp

## Building the DApp

The `requirements.txt` file has all python dependencies with version pinned, and was generated from `requirements.in` file by [pip-tools](https://pip-tools.readthedocs.io/en/latest/). This is done in order to ensure the inference code will use the same versions used during training, improving reproducibility.

Since there is no official pre-built wheels for RISC-V published in PyPI for packages like NumPy and TensorFlow Lite, we have built these packages externally and published in GitHub. The first line of the `requirements.txt` file will instruct pip to look at this github repository for these pre-built wheels, and use them. This way, the build process works by just issuing the regular build command:

```console
docker buildx bake --load
```

## Running unit tests inside the Cartesi VM

In the local development environment, running test is as simple as calling `python -m unittest`. However, to run them in its production environment inside the Cartesi VM, you can spawn a console session perform the same command:

```console
$ docker run --rm -it cartesi/dapp:tflite-image-classifier-devel-console
Running in interactive mode!
         .
        / \
      /    \
\---/---\  /----\
 \       X       \
  \----/  \---/---\
       \    / CARTESI
        \ /   MACHINE
         '
$ cd /opt/cartesi/dapp
$ python -m unittest
..
----------------------------------------------------------------------
Ran 2 tests in 5.669s

OK
```

This can also be done in a single command:

```console
docker run -it --name=tflite-image-classifier-benchmark \
    cartesi/dapp:tflite-image-classifier-devel-console \
        cartesi-machine --ram-length=128Mi \
                        --rollup \
                        --flash-drive=label:root,filename:dapp.ext2 \
                        --ram-image=linux.bin \
                        --rom-image=rom.bin -i \
                        -- "cd /opt/cartesi/dapp; python -m unittest"
```

## Interacting with the application

This dapp expects the raw image data as input. To make the process easier,
the script `send_file_as_input.py` is supplied. Once the dapp is running, this
script can be used as below:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install web3
python3 send_file_as_input.py tests/grace_hopper.jpg
```

To retrieve the notices, we can use the [frontend-console](https://github.com/cartesi/rollups-examples/tree/main/frontend-console) application, from the cartesi/rollups-example repository, to interact with the DApp.
Ensure that the [application has already been built](https://github.com/cartesi/rollups-examples/blob/main/frontend-console/README.md#building) before using it.

First, go to a separate terminal window and switch to the `frontend-console` directory:

```shell
cd frontend-console
```

Then retrieve the results for the inference that were sent as a notice, with the command:

```shell
yarn start notice list
```

## Running the environment in host mode

When developing an application, it is often important to easily test and debug it. For that matter, it is possible to run the Cartesi Rollups environment in [host mode](../README.md#host-mode), so that the DApp's back-end can be executed directly on the host machine, allowing it to be debugged using regular development tools such as an IDE.

This DApp's back-end is written in Python, so to run it in your machine you need to have `python3` installed.

In order to start the back-end, run the following commands in a dedicated terminal:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 -m dapp.dapp
```

The final command will effectively run the back-end and send corresponding outputs to port `5004`.
It can optionally be configured in an IDE to allow interactive debugging using features like breakpoints.

You can also use a tool like [entr](https://eradman.com/entrproject/) to restart the back-end automatically when the code changes. For example:

```shell
ls *.py | ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" entr -r python3 -m dapp.dapp
```

After the back-end successfully starts, it should print an output like the following:

```log
INFO:__main__:HTTP rollup_server url is http://127.0.0.1:5004
INFO:__main__:Sending finish
```

After that, you can interact with the application normally [as explained above](#interacting-with-the-application).
