from __future__ import print_function, division
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter


class OutputUtils:

    def __init__(self, image_dir, log_dir):
        """
        :param image_dir: path for saving images (if any)
        :param log_dir: path for saving tensorboard data
        """
        self.image_dir = image_dir
        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
        os.makedirs(image_dir)

        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
        os.makedirs(log_dir)
        self.tb_writer = SummaryWriter(log_dir)

        self.image_count = 0

    # TODO example in case we want to log
    def write_tensorboard_statistics(self, step, model_loss, deep_recon_loss,
                                     down_shallow_recon_losses, down_intelligibility_losses,
                                     up_shallow_recon_losses, up_intelligibility_losses):
        self.tb_writer.add_scalar("Deep Reconstruction Loss", deep_recon_loss, step)
        self.tb_writer.add_scalar("Combined Reconstruction Loss", model_loss, step)
        self.tb_writer.add_scalars("Down Shallow Reconstruction Loss", down_shallow_recon_losses, step)
        self.tb_writer.add_scalars("Down Intelligibility Loss", down_intelligibility_losses, step)
        self.tb_writer.add_scalars("Up Shallow Reconstruction Loss", up_shallow_recon_losses, step)
        self.tb_writer.add_scalars("Up Intelligibility Loss", up_intelligibility_losses, step)

    @staticmethod
    def imshow_common(img, is_tensor=False):
        np_img = img
        if is_tensor:
            img = img / 2 + 0.5
            np_img = img.numpy()
            np_img = (np_img * 255).astype(np.uint8)
        plt.axis('off')
        return np_img

    def imshow(self, img, title=None):
        np_img = self.imshow_common(img)
        plt.imshow(np.transpose(np_img, (1, 2, 0)))
        if title:
            plt.title(title)

    def imshow_single_channel(self, img, title=None):
        np_img = self.imshow_common(img)
        plt.imshow(np_img)
        if title:
            plt.title(title)

    def write_image_to_file(self, tensor, title, output_dir, single_channel=False):
        fig = plt.figure()
        plt.title(title)
        if single_channel:
            self.imshow_single_channel(tensor, title=title)
        else:
            self.imshow(tensor, title)
        img_name = output_dir + title + ".png"
        plt.savefig(img_name)
        plt.close(fig)
        plt.clf()

    def write_image_to_tensorboard(self, tensor, title, tb_step):
        print(f"write image {self.image_count}")
        self.image_count += 1
        fig = plt.figure()
        # plt.title(title)
        self.imshow(tensor, title)
        self.tb_writer.add_figure(tag=title, figure=fig, global_step=tb_step)
