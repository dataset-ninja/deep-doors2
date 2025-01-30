Dataset **DeepDoors2** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM1NjRfRGVlcERvb3JzMi9kZWVwZG9vcnMyLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogInlhQW9KREVCamIxK29NQzRlUytldzZEZnVVdFF4ekF2cFlDbWQyRGdCM3M9In0=)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='DeepDoors2', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://drive.google.com/drive/folders/1SxVKeJ9RBcoJXHSHw-LWaLGG07BZT-b5?usp=sharing).