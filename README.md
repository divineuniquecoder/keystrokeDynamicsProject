# keystrokeDynamicsProject
Repository for the final year project on biometric behavioural continuous user authentication. This project develops and tests a system designed to authenticate users based on their unique keystroke dynamics, incorporating real-time data analysis and machine learning techniques to enhance security.

Project Title: Continuous User Authentication System
Overview
This repository contains the code and resources for a Continuous User Authentication (CUA) system that utilises keystroke dynamics and a Support Vector Machine (SVM) model. The project is designed to validate the functionality, reliability, and security of authentication processes under various scenarios.

Repository Structure

Keystrokes Data Collection Implementation – "keystrokesMetrics"
Core Functionality Files:
1.	mainApp.py: The main application file integrating all system components.
2.	sessionManager.py: Manages user sessions and handles session timeouts.
3.	taskManager.py: Coordinates tasks within the system.
4.	userInterface.py: Manages user interface interactions.
5.	authenticationManager.py: Manages the authentication processes.
6.	dataCollector.py: Gathers and organizes user data for processing.
Purpose: Manage the main application logic, user session handling, task coordination, user interactions, and data collection.

Database and Configuration Management Files:
1.	dataBase.py: Manages database operations.
2.	configManager.py: Manages application configurations stored in config.json.
Purpose: Handle all database interactions and configuration settings management.

Error Handling and Logging Files (errorHandler.py): Manages and logs errors throughout the system.
Purpose: Provide robust error handling and system-wide logging capabilities.

User and Task Management Files:
1.	imporTALLUSERS.py, specificuser.py: Scripts for managing user data.
2.	specificTask.py: Manages specific tasks within the system.
3.	userALL.csv: Contains user data for the system.
Purpose: Manage user and task-related data and operations.

Firebase Integration Files:
1.	akinprojectsecurity-firebase-adminsdk-useyours.json: Contains Firebase service account credentials.
2.	firebaseImportSPECIFICUSERS.py: Manages the import of specific user data via Firebase.
Purpose: Securely integrate and manage Firebase services.
Run the application: python mainApp.py



SVM Implementation and Model Testing – "modelTraining"
Files:
1.	theSVM.py, onewithSVM.py: Implement and execute the SVM model.
2.	forTesting.py: checks for user data validation
3.	bigramcounts.py: Generates bi-gram counts, essential for feature extraction.
4.	statisticsrawdatauserALL.py: Provides statistical analysis of raw data.
5.	flighttimestat.py: Analyses keystroke flight times.
Purpose: Develop, test, and refine the SVM-based authentication to enhance security and accuracy.

Data Preparation and Analysis Files:
1.	metricsCalculation.py: Calculates and analyses keystroke metrics.
2.	dataCollector.py: Gathers and organises user data during testing.
Purpose: Prepare and analyse data to support SVM model training and testing.

Run the application: Each Python file can be run individually

Testing Folder Overview - forLiveCUA_Test
Purpose:
Contains all scripts and data files necessary for evaluating the CUA system.
Included Files and Their Purpose:
1.	metricsCalculation.py - Calculates and analyses keystroke metrics from user data.
2.	output.csv - Initial output data file capturing raw test results.
3.	postProcessed.csv - Data file showing results after post-processing steps have been applied.
4.	preprocessed.py - Script for preprocessing input data before it is fed into the authentication model.
5.	sessionManager.py - Manages user sessions, tracking active users and handling session timeouts.
6.	SVM.py - Core script containing the SVM model implementation for user authentication.
7.	svm11.pkl - Serialized version of the trained SVM model ready for deployment.
8.	taskManager.py - Coordinates different tasks within the authentication process.
9.	theOutput.csv - Final output file containing processed and validated results.
10.	userInterface.py - Manages the user interface interactions, providing a bridge between the user and the system operations.
Configuration and Firebase Integration:
1.	akinprojectsecurity-firebase-adminsdk-useyours.json - Contains the Firebase service account credentials required for securely connecting to Firebase services.
2.	authenticationManager.py - Manages authentication processes, ensuring all authentication steps are secure and efficient.
3.	conAuthen.py - Specialized script for conducting and managing continuous authentication tests.
4.	config.json - Configuration file that holds system settings and external API links.
5.	configManager.py - Handles the loading and management of configuration settings from config.json.
6.	dataBase.py - Manages interactions with the database.
7.	dataCollector.py - Gathers and organises user data during testing.
8.	errorHandler.py - Manages and logs errors throughout the testing process.
9.	importData.py - Facilitates the importation of necessary data sets for testing.
10.	mainApp.py - The main application file that integrates all components of the system for full-scale system testing.
Run the application: python mainApp.py
