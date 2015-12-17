#NeuralTalkTheano

This project contains *Python+numpy+theano* source code for learning **Multimodal Recurrent Neural Networks** that describe images / Videos with sentences.
Code structure is derived from the original neuraltalk code relased by Andrej Karpath at https://github.com/karpathy/neuraltalk but the implementations is based 
on theano and hence can run on GPU's

This code was used in our entry for the LSMDC Challenge and described in the paper "Video captioning with recurrent networks based on frame- and video-level features and visual content classification" (http://arxiv.org/abs/1512.02949)

# Instruction on using the code

1. Checkout the code using git
2. Make sure you have theano installed and working. As a quick check "import theano" should work without any errors on a python shell
3. The code expects the data files to be in "data/<dataset_name>" directory. It needs a .json file containing all the training/validation/test samples and we need a .mat feature file containin the CNN image / dense trajectory video features for each sample. Actual images are only needed for visualisation of results and are not needed during training. (For Aalto users sample dataset.json and feature file can be found in /triton/ics/project/imagedb/picsom/databases/COCO/analysis/shettyr1 directory for COCO dataset)
4. Now you have everything you need. You can start the training by running the driver_theano.py file. To see the input options run "python driver_theano.py --help". Sample command is below:
	
	python driver_theano.py -d coco -l 0.404e-3 --decay_rate 0.999 --grad_clip 10.0 --image_encoding_size 600 --word_encoding_size 600 --hidden_size 600 -o cvCoco/layer6/ --fappend c_in14_o6_fc7_d_c --worker_status_output_directory statusCoco --write_checkpoint_ppl_threshold 20 --regc 2.66e-07 --batch_size 64 --eval_period 0.5 --max_epochs 30 --feature_file feat_new_fc7_4096.mat --image_feat_size 4096 --data_file dataset.json --mat_new_ver 

5. You can monitor the training using monitor_cv.html. Make sure to point it to the right status file. Instructions from original neuraltalk code given below:
	- "The status can be inspected manually by reading the JSON and printing whatever you wish in a second process. In practice I run cross-validations on a cluster, so my `cv/` fold    er fills up with a lot of checkpoints that I further filter and inspect with other scripts. I am including my cluster training status visualization utility as well if you like. Run a local webserver (e.g.     `$ python -m SimpleHTTPServer 8123`) and then open `monitorcv.html` in your browser on `http://localhost:8123/monitorcv.html`, or whatever the web server tells you the path is. You will have to edit the     file to setup the paths properly and point it at the right json files"
6. Once the training is complete ( or even during training) you can use the checkpoint files saved (default in cv/ folder) to evaluate the model on test dataset or use it to predict on arbitrary images. 
	- To run evaluation on test images use eval_sentence_predictions.py. (Eg python eval_sentence_predictions.py cvCoco/layer6/model_checkpoint_coco_gpu004_c_in14_o6_fc6_d_c_11.35.p --result_struct_filename result_coco_theano_fc6.json)

7. To use the model to do predictions on arbitrary images use the predict_on_images.py script. See the instruction below:
	
	Usage is as follows : 
	
	python predict_on_images.py <checkpoint file name> -i <text file with list of images> -f <feature file> -d <output directory> --fname_append <String to append to output files>
	
	Eg usage: python predict_on_images.py cvCoco/layer6/model_checkpoint_coco_gpu004_c_in14_o6_fc7_d_c_11.08.p -i imgListCOCO_bin.txt -f /triton/ics/project/imagedb/picsom/databases/COCO/analysis/shettyr1/../../features/c_in14_o6_fc7_d_c.bin -d example_images/ --fname_append fc7_d_c_11p080
	
	The input text file can either have list images or list of images and corresponding index in the feature file with comma seperation. If it is just images indices are assumed from 0:N. 
	
	Eg: 
	
	./example_images/89pUfSc.jpg, 1 (index in feature file)
	./example_images/animals.jpg, 2
	./example_images/cobra.jpg, 4
	./example_images/mic.jpg, 10
	
	or 
	
	./example_images/89pUfSc.jpg
	./example_images/animals.jpg
	./example_images/cobra.jpg
	./example_images/mic.jpg
	
	Also it supports both the feature file types i.e .mat files and .bin files in picsom format. For .bin file I used the script picsom_bin_data.py with some modifications (It is also in the same directory).
	
	The output is a .json file and .html file with visualisations. For eg: (triton/ics/project/imagedb/picsom/databases/image-net/analysis/shettyr1/neuraltalkTheano/example_images/result_fc7_d_c_11p080.html)

	
8. The code also supports many features like training deep lstm n/w, output vocabulary factorization and variations like training a seperate evaluator network etc, but this is not well documentated yet! ( Hopefully I will be able to describe these in detail and relase a documentation)  

