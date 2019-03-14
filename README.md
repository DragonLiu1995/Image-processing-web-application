# Image-processing-web-application
1. Effects to achieve
       This project focuses on image segmentation based on 3 methods, respectively Ostu’s method, Kmeans algorithm and Gaussian Mixture
       Model. <br>
2. Details of algorithm(All algorithms are implemented by myself)<br>
       i) In Ostu’s method, I used the method covered in class and just pick a threshold that maximizes the between-class variance.<br>
       ii) In Kmeans algorithm, I optimize the initialization using Kmeans++ initialization method proposed by David Arthur and 
       Sergei Vassilvitskii. The model is encapsulated in kmeans.py<br>
       iii) In Gaussian Mixture Model, I implement the EM algorithm, which iteratively computing E-step and M-step. E-step computes the mixture probabilities for all data points while M-step updates the means, covariance matrices and prior probabilities. The initialization schemes also use kmeans algorithm that only runs one step in order to achieve good initial parameter settings. The model is encapsulated in EM.py<br><br>
3. Instruction on how to run this program<br>
Step 1:
   This is an image processing web application which are embedded in Flask framework. Before running this web app, please make sure that you install Flask
   backend services.<br>
   To install Flask, just type “pip install Flask” in your command line or terminal. Other packages include cv2, numpy and scipy.<br>
Step 2:
   To run this program, type in your command line “cd ‘root directory of this application(where app.py resides)’. Inside your root directory, type in your
command line “python app.py”, then the application will be hosted on your localhost, and port by default is 8080, as shown in Fig 1.
(If port 8080 is preempted by another application, you can change this configuration in app.py. Find this line app.run(host='localhost', port=8080, debug=True), and
change the port number to any other available ports from 0 to 65535.)
