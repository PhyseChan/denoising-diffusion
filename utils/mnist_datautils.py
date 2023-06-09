import torch as tr
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor, Compose
from torch.utils.data.distributed import DistributedSampler


class Dequantize(object):
    def __call__(self, x):
        x = (x + tr.randint(0, 256, x.shape)/256. ) / 256.
        return x
    
def get_dataloader(path, batch_size, transform=None, ddp=False):
    if transform is None:
        transform=Compose([
            ToTensor(),
            Dequantize()
            ])
    else:
        transform = transform
    dataset = MNIST(path, transform=ToTensor(), download=True)
    if ddp:
        sampler = DistributedSampler(dataset, shuffle=True)
    else:
        sampler = None
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=bool(~ddp), sampler=sampler)
    return dataloader