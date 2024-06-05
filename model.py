import torch
import torch.nn as nn
from Aggregation_layers import L2Norm, Flatten, GeM
import torchvision.models as models


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

