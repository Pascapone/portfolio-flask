from sklearn.datasets import make_blobs
import numpy as np
import random
import sys

def create_clusters(n_samples=50, centers=2, cluster_std=1):
    points = make_blobs(n_samples=n_samples, n_features=2, centers=centers, cluster_std=cluster_std, center_box=(-20.0, 20.0))[0]
    return points.tolist()


def knearest(points, move_percentage=0.7, early_stopping_threshold=0.01, iterations=40, runs=150, centers=5, center_box=(-20.0, 20.0)):  
    
    def calculate_distance(point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

    def initialize_random_classifiers(centers, center_box):
        classifiers = []
        for _ in range(centers):
            x = random.random()*(center_box[1] - center_box[0]) + center_box[0] 
            y = random.random()*(center_box[1] - center_box[0]) + center_box[0] 
            classifiers.append([x, y, 0, 0]) 
            
        return classifiers
    
    def find_parent_classifiers(points, classifiers):
        points[:, 2:] = -1
        for point in points:
            for i, classifier in enumerate(classifiers):
                distance = calculate_distance(point, classifier)               

                if point[3] == -1 or point[3] > distance:
                    point[2] = i
                    point[3] = distance 
                    
        for i, classifier in enumerate(classifiers):     
            x_avg = np.average(points[points[:, 2] == i, 0])
            y_avg = np.average(points[points[:, 2] == i, 1])     
            classifier[2] = 0 if np.isnan(x_avg) else x_avg      
            classifier[3] = 0 if np.isnan(y_avg) else y_avg               
                    
    def move_classifiers_towards_center_of_mass(classifiers, move_percentage):
        for classifier in classifiers:     
                if not np.isnan(classifier[2]):
                    x_dir = classifier[2] - classifier[0]
                    y_dir = classifier[3] - classifier[1]
                    classifier[0] += x_dir*move_percentage
                    classifier[1] += y_dir*move_percentage
                    
    def calculate_cost(points, classifiers):
        distance_sum = 0
        for i, _ in enumerate(classifiers):
            classifier_distances = points[points[:, 2] == i, 3]

            distance_sum += np.sum(classifier_distances)

        return distance_sum

    points = np.concatenate((points, (np.ones(shape=[points.shape[0], 2])*-1)), axis=1)
    run_tracker = []
    for run in range(runs): 
        points[:, 2:] = -1
        classifiers = initialize_random_classifiers(centers, center_box)
        
        iteration_tracker = []
        old_classifiers = []
        for _ in range(iterations):    
            old_classifiers = [classifier.copy() for classifier in classifiers]
            find_parent_classifiers(points, classifiers)
            
            iteration_tracker.append((points.copy(), [classifier.copy() for classifier in classifiers]))
            
            move_classifiers_towards_center_of_mass(classifiers, move_percentage)   

            counter = 0
            for classifier, old_classifier in zip(classifiers, old_classifiers):
                if calculate_distance(classifier, old_classifier) <= early_stopping_threshold:
                    counter += 1
            if counter == len(classifiers):
                break
                
        run_tracker.append({'run' : run, 'cost' : calculate_cost(points, classifiers), 'points' : points.copy(), 
                            'classifiers' : classifiers.copy(), "iteration_tracker" : iteration_tracker.copy()})
    
    return run_tracker