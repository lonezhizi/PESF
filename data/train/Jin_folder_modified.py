import os
import glob
import shutil
import fnmatch
root_path = "C:\\pycharm workspace\\SAM-Med3D-main\\data\\train"

# folder_names = ["spleen",
#         "kidney_right",
#          "kidney_left",
#          "gallbladder",
#          "liver",
#          "stomach",
#          "pancreas",
#          "adrenal_gland_right",
#          "adrenal_gland_left",
#          "lung_upper_lobe_left",
#          "lung_lower_lobe_left",
#          "lung_upper_lobe_right",
#          "lung_middle_lobe_right",
#          "lung_lower_lobe_right",
#          "esophagus",
#          "trachea",
#          "thyroid_gland",
#          "small_bowel",
#          "duodenum",
#          "colon",
#          "urinary_bladder",
#          "prostate",
#          "kidney_cyst_left",
#          "kidney_cyst_right",
#          "sacrum",
#          "vertebrae_S1",
#          "vertebrae_L5",
#          "vertebrae_L4",
#          "vertebrae_L3",
#          "vertebrae_L2",
#          "vertebrae_L1",
#          "vertebrae_T12",
#          "vertebrae_T11",
#          "vertebrae_T10",
#          "vertebrae_T9",
#          "vertebrae_T8",
#          "vertebrae_T7",
#          "vertebrae_T6",
#          "vertebrae_T5",
#          "vertebrae_T4",
#          "vertebrae_T3",
#          "vertebrae_T2",
#          "vertebrae_T1",
#          "vertebrae_C7",
#          "vertebrae_C6",
#          "vertebrae_C5",
#          "vertebrae_C4",
#          "vertebrae_C3",
#          "vertebrae_C2",
#          "vertebrae_C1",
#          "heart",
#          "aorta",
#          "pulmonary_vein",
#          "brachiocephalic_trunk",
#          "subclavian_artery_right",
#          "subclavian_artery_left",
#          "common_carotid_artery_right",
#          "common_carotid_artery_left",
#          "brachiocephalic_vein_left",
#          "brachiocephalic_vein_right",
#          "atrial_appendage_left",
#          "superior_vena_cava",
#          "inferior_vena_cava",
#          "portal_vein_and_splenic_vein",
#          "iliac_artery_left",
#          "iliac_artery_right",
#          "iliac_vena_left",
#          "iliac_vena_right",
#          "humerus_left",
#          "humerus_right",
#          "scapula_left",
#          "scapula_right",
#          "clavicula_left",
#          "clavicula_right",
#          "femur_left",
#          "femur_right",
#          "hip_left",
#          "hip_right",
#          "spinal_cord",
#          "gluteus_maximus_left",
#          "gluteus_maximus_right",
#          "gluteus_medius_left",
#          "gluteus_medius_right",
#          "gluteus_minimus_left",
#          "gluteus_minimus_right",
#          "autochthon_left",
#          "autochthon_right",
#          "iliopsoas_left",
#          "iliopsoas_right",
#          "brain",
#          "skull",
#          "rib_right_4",
#          "rib_right_3",
#          "rib_left_1",
#          "rib_left_2",
#          "rib_left_3",
#          "rib_left_4",
#          "rib_left_5",
#          "rib_left_6",
#          "rib_left_7",
#          "rib_left_8",
#          "rib_left_9",
#          "rib_left_10",
#          "rib_left_11",
#          "rib_left_12",
#          "rib_right_1",
#          "rib_right_2",
#          "rib_right_5",
#          "rib_right_6",
#          "rib_right_7",
#          "rib_right_8",
#          "rib_right_9",
#          "rib_right_10",
#          "rib_right_11",
#          "rib_right_12",
#          "sternum",
#          "costal_cartilages"]

folder_names = ['adrenal_gland_left',
                'adrenal_gland_right',
                'aorta',
                'urinary_bladder',
                'colon',
                'duodenum',
                'esophagus',
                'femur_left',
                'femur_right',
                'gallbladder',
                'inferior_vena_cava',
                'kidney_left',
                'kidney_right',
                'liver',
                'pancreas',
                'portal_vein_and_splenic_vein',
                'prostate',
                'spleen',
                'stomach']


def create_folders(folder_names):
    for folder_name in folder_names:
        os.mkdir(folder_name)



def create_sub_folder(root_path,requided_folder):  ###在117个类的各类文件夹中创建以数据集命名的文件夹

   #ref_filefolder_list = os.listdir(root_path)
   for sub_filefolder_name in folder_names:
      absulute_path=root_path+"\\"+sub_filefolder_name+"\\"+requided_folder    ###C:\pycharm workspace\SAM-Med3D-main\data\train\brain\BTCV
      os.mkdir(absulute_path)


def create_subsub_folder(root_path,dataset_name, requided_folder1, requided_folder2):####在以数据集命名的文件夹中在创建 imagesTr和labelsTr子文件夹
   for sub_filefolder_name in folder_names:
       absulute_path1 = root_path+"\\"+sub_filefolder_name+"\\"+ dataset_name +"\\" + requided_folder1
       absulute_path2 = root_path + "\\" + sub_filefolder_name + "\\" + dataset_name +"\\" + requided_folder2
       os.mkdir(absulute_path1)
       os.mkdir(absulute_path2)

def remove_file(inputimageTr_path,inputiamgeLabl_path, datasetname):
    input_imageTr_path_list = glob.glob(os.path.join(inputimageTr_path,'*.gz')) ###获得文件的训练数据的路径
    input_imageTr_name = glob.glob1(inputimageTr_path,'*.nii.gz') ###获得训练数据名
    for organ_name in folder_names:
      output_imageTr_path = root_path+ "\\" + organ_name + "\\" + datasetname + "\\" + "imagesTr"
      for image_name in input_imageTr_path_list: ####复制train data 到 每一个子文件夹
          #if len(os.listdir(output_imageTr_path)) == 0:##如果训练文件夹是空，则进行复制
           shutil.copy(image_name,output_imageTr_path)

      #output_imageLabl_path = root_path+ "\\" + organ_name + "\\" + datasetname + "\\" + "labelsTr"  ####'C:\\pycharm workspace\\SAM-Med3D-main\\data\\train\\spleen\\BTCV\\labelsTr'

      for input_file_name in input_imageTr_name:
          inputindex = input_file_name.split(".")[0]
          input_imageLabl_sub_path = inputiamgeLabl_path + "\\" + inputindex
          input_image_organ_path = []
          for root, dirs, files in os.walk(input_imageLabl_sub_path):
              for file in files:
                  #filename = organ_name +'.nii.gz'
                  #if  fnmatch.fnmatch(file, filename):
                input_image_organ_path = os.path.join(root,file)
                sub_organ_name = file[:-7]
                  #if len(os.listdir(output_imageLabl_path)) == 0:
                 ###shutil.copy(input_image_organ_path,output_imageLabl_path)
                output_imagelabl_path = root_path + "\\" + sub_organ_name + "\\" + datasetname+ "\\" + "labelsTr"
                newname = output_imagelabl_path+ "\\" + input_file_name
                os.rename(input_image_organ_path, newname) #####移动并重命名该文件






    #print(imageTr_name)
    return

##############step:111111##################
#create_folders(folder_names)###创建117个类的子文件夹

##############step:2222222###################
#create_sub_folder(root_path,"WORD") ###在117个类文件夹中创建以数据集（BTCV,Amos...）命名的文件夹

################step:33333333#################
#create_subsub_folder(root_path,"WORD", "imagesTr", "labelsTr")


#remove_file("C:\\pycharm workspace\\SAM-Med3D-main\\data\\BTCV_TrTs_UnlabeledCase","C:\\pycharm workspace\\SAM-Med3D-main\\data\\BTCV_Pseudo_label_117classes","BTCV")
remove_file("C:\\pycharm workspace\\SAM-Med3D-main\\data\\nnU-NetStyle-valdata\\WORD\\imagesVl","C:\\pycharm workspace\\SAM-Med3D-main\\data\\Totalsegmentator_sam_valdataset\\WORD_19cls_pseudo","WORD")


