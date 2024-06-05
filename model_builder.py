import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
import torchvision.models as models

#Generalized Mean Pooling Layer
class GeM(nn.Module):
    def __init__(self, p=3, eps=1e-6):
        super(GeM,self).__init__()
        self.p = nn.Parameter(torch.ones(1)*p)
        self.eps = eps

    def forward(self, x):
        return self.gem(x, p=self.p, eps=self.eps)
        
    def gem(self, x, p=3, eps=1e-6):
        return F.avg_pool2d(x.clamp(min=eps).pow(p), (x.size(-2), x.size(-1))).pow(1./p)
        
    def __repr__(self):
        return self.__class__.__name__ + '(' + 'p=' + '{:.4f}'.format(self.p.data.tolist()[0]) + ', ' + 'eps=' + str(self.eps) + ')'
    
# Flattening Layer
class Flatten(torch.nn.Module):
    def __init__(self):
        super().__init__()
    
    def forward(self, x):
        assert x.shape[2] == x.shape[3] == 1, f"{x.shape[2]} != {x.shape[3]} != 1"
        return x[:, :, 0, 0]

# L2 Normalisation layer
class L2Norm(nn.Module):
    def __init__(self, dim=1):
        super().__init__()
        self.dim = dim
    
    def forward(self, x):
        return F.normalize(x, p=2.0, dim=self.dim)
    


# To remember, we need to create a datapipeline because Resnets expect a specific format as input, check this link for more info:
# https://pytorch.org/hub/pytorch_vision_resnet/


# The number of channels in the last convolutional layer, the one before average pooling
CHANNELS_NUM_IN_LAST_CONV = {
    "ResNet18": 512,
    # Add more architectures here if needed
}

class Model(nn.Module):
    def __init__(self, backbone_name, out_dim):
        super(Model, self).__init__()
        assert backbone_name in CHANNELS_NUM_IN_LAST_CONV, f"backbone must be one of {list(CHANNELS_NUM_IN_LAST_CONV.keys())}"
        #self.backbone = models.resnet18(weights=True)
        self.backbone = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        #self.backbone.fc = nn.Identity()  # Replace the classifier with an identity function
        in_dim = CHANNELS_NUM_IN_LAST_CONV[backbone_name]

        self.feature_agg=nn.Sequential(
            L2Norm(),
            GeM(),
            Flatten(),
            nn.Linear(in_dim, out_dim),
            L2Norm()
        )

    def forward(self, x):
        x = self.backbone(x)
        x = self.feature_agg(x)
        return x

