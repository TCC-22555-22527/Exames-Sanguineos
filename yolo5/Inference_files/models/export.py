"""Exports a YOLOv5 *.pt model to ONNX and TorchScript formats

Usage:
    $ export PYTHONPATH="$PWD" && python models/export.py --weights ./weights/yolov5s.pt --img 640 --batch 1 # noqa: E501
"""

import argparse

import torch
from utils.google_utils import attempt_download

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str,
                        default='./yolov5s.pt', help='weights path')
    parser.add_argument('--img-size', nargs='+', type=int,
                        default=[640, 640], help='image size')
    parser.add_argument('--batch-size', type=int, default=1, help='batch size')
    opt = parser.parse_args()
    opt.img_size *= 2 if len(opt.img_size) == 1 else 1  # expand
    print(opt)

    # Input
    # image size(1,3,320,192) iDetection
    img = torch.zeros((opt.batch_size, 3, *opt.img_size))

    # Load PyTorch model
    attempt_download(opt.weights)
    model = torch.load(opt.weights, map_location=torch.device('cpu'))[
        'model'].float()
    model.eval()
    model.model[-1].export = True  # set Detect() layer export=True
    y = model(img)  # dry run

    # TorchScript export
    try:
        print('\nStarting TorchScript export with torch %s...' %
              torch.__version__)
        f = opt.weights.replace('.pt', '.torchscript.pt')  # filename
        ts = torch.jit.trace(model, img)
        ts.save(f)
        print('TorchScript export success, saved as %s' % f)
    except Exception as e:
        print('TorchScript export failure: %s' % e)

    # ONNX export
    try:
        import onnx

        print('\nStarting ONNX export with onnx %s...' % onnx.__version__)
        f = opt.weights.replace('.pt', '.onnx')  # filename
        model.fuse()  # only for ONNX
        torch.onnx.export(model, img, f, verbose=False, opset_version=12, input_names=['images'],  # noqa: E501
                          output_names=['classes', 'boxes'] if y is None else ['output'])  # noqa: E501

        # Checks
        onnx_model = onnx.load(f)  # load onnx model
        onnx.checker.check_model(onnx_model)  # check onnx model
        # print a human readable model
        print(onnx.helper.printable_graph(onnx_model.graph))
        print('ONNX export success, saved as %s' % f)
    except Exception as e:
        print('ONNX export failure: %s' % e)

    # CoreML export
    try:
        import coremltools as ct

        print('\nStarting CoreML export with coremltools %s...' % ct.__version__)  # noqa: E501
        # convert model from torchscript and apply pixel scaling as per detect.py # noqa: E501
        model = ct.convert(ts, inputs=[ct.ImageType(
            name='images', shape=img.shape, scale=1 / 255.0, bias=[0, 0, 0])])
        f = opt.weights.replace('.pt', '.mlmodel')  # filename
        model.save(f)
        print('CoreML export success, saved as %s' % f)
    except Exception as e:
        print('CoreML export failure: %s' % e)

    # Finish
    print('\nExport complete. Visualize with https://github.com/lutzroeder/netron.')
