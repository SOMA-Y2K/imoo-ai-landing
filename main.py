import os
import sys
sys.path.append("/home/soma5/miniconda3/lib/python3.10/site-packages/opencv")

def run_main_script(input_value) : 
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    os.system("python3 -m torch.distributed.run --standalone --nproc_per_node=1 test_warping.py \
        --name test_partflow_vitonhd_unpaired_1109 \
        --PBAFN_warp_checkpoint 'checkpoints/gp-vton_partflow_vitonhd_usepreservemask_lrarms_1027/PBAFN_warp_epoch_121.pth' \
        --resize_or_crop None --verbose --tf_log \
        --batchSize 2 --num_gpus 1 --label_nc 14 --launcher pytorch \
        --dataroot VITON-HD \
        --image_pairs_txt test_pairs_unpaired_1018.txt")



    os.system(f"python3 -m torch.distributed.run --standalone --nproc_per_node=1 --master_port=4736 test_tryon.py \
        --name {input_value} \
        --resize_or_crop None --verbose --tf_log --batchSize 12 --num_gpus 1 --label_nc 14 --launcher pytorch \
        --PBAFN_gen_checkpoint 'checkpoints/gp-vton_gen_vitonhd_wskin_wgan_lrarms_1029/PBAFN_gen_epoch_201.pth' \
        --dataroot VITON-HD \
        --image_pairs_txt test_pairs_unpaired_1018.txt \
        --warproot sample/test_partflow_vitonhd_unpaired_1109/")



