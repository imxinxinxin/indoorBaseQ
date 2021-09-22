Copyright (c) 2018, Universitat Jaume I (UJI)
These data is licensed under CC Attribution 4.0 International (CC BY).
This documentation is licensed under CC0 license.


This folder contains the WiFi RSS fingerprint data described in <Long-Term Wi-Fi fingerprinting dataset for robust indoor positioning,G.M. Mendoza-Silva et al., 2017> and available at Zenodo repository, DOI 10.5281/zenodo.1066041.

* Each subfolder contains the measurements of each dataset that belongs to a collection month.
* Each dataset is represented by four files: the RSS, the time, the coordinates, and the identifiers files, so that the ith row of each of them holds the respective information of the ith fingerprint of the dataset.
* Each column in the RSS file represents intesity measurement values (dBm) for a specific wireless access point. If the access point was not detected for a fingerprint, its intensity value is 100 in that fingerprint.
* The naming convention for representing a dataset is 'dddnnttt.csv', where ddd is either 'trn' (training) or 'tst' (test), nn is two a two digit number (e.g., '01'), and ttt is the dataset' information contained in the file, which can be 'rss' for a RSS information file, 'crd' for coordinates file, 'tms' for the time file, and 'ids' for the identifiers file.
* Most of samples were collected using a Samsung Galaxy S3 smartphone. Only files corresponding to training 2 and tests 6-10 from month 25 were collected using a Samsung Galaxy A5 (2017) smartphone.

这个文件夹包含了在<长期Wi-Fi指纹数据集的鲁棒室内定位，G.M.描述的WiFi RSS指纹数据Mendoza-Silva等人，2017>，可在Zenodo存储库获取，DOI 10.5281/ Zenodo .1066041。
*每个子文件夹包含每个数据集属于一个收集月的测量值。
*每个数据集由四个文件表示:RSS文件、时间文件、坐标文件、标识符文件，每个文件的第i行分别存放数据集第i个指纹的信息。
* RSS文件中的每一列代表特定无线接入点的intesity测量值(dBm)。如果没有检测到指纹的接入点，其强度值在该指纹中为100。
*表示数据集的命名约定为'dddnnttt。ddd是csv”,即“环境”(培训)或“测试”(测试),神经网络是二百一十二位数(例如,“01”),以及ttt是数据集的信息中包含的文件,可以“rss”rss信息文件,crd的坐标文件,“颅磁刺激”的文件,文件和“id”标识。
*大部分样本是使用三星Galaxy S3智能手机采集的。仅使用三星Galaxy A5(2017)智能手机收集第25个月培训2和测试6-10对应的文件。