#FROM ubuntu:23.10
FROM continuumio/miniconda3

RUN conda install -c conda-forge pip
COPY signalp-6-package/ /signalp-6-package/
#COPY site-packages/ /site-packages/
#RUN pip install -r /signalp-6-package/requirements.txt -e /site-packages/
RUN pip install /signalp-6-package/ -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN SIGNALP_DIR=$(python3 -c "import signalp; import os; print(os.path.dirname(signalp.__file__))" ) && mv /signalp-6-package/models/distilled_model_signalp6.pt $SIGNALP_DIR/model_weights/ #一定要用&&，因为隔一层，参数就不能传递识别了
#COPY signalp-6-package/models/distilled_model_signalp6.pt $SIGNALP_DIR/model_weights/

RUN rm -rf /signalp-6-package/

CMD ["/bin/bash"]


