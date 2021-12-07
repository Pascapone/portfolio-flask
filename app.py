# backend/app.py
import os, sys

from flask import Flask, request
from mnist_classifier import classify_mnist_image
from imagenet_classifier import classify_image
import json
from astar_pathfinding import find_path
from grid import create_grid
from knearest import create_clusters, knearest
import numpy as np
from flask_cors import CORS

node_config = json.load(open('./pathfinding.json', 'r'))

MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = 'http://localhost:3000/'

app = Flask(__name__)

CORS(app)

# Ignore static folder in development mode.
if MODE == "development":
    app = Flask(__name__, static_folder=None)

@app.route('/api-classify-mnist', methods=['POST'])
def classify_mnist():    
    if (request.data): 
        image = request.data
        result = classify_mnist_image(image)
        print('Model classification: ' + result)        
        return result

@app.route('/api-classify-image', methods=['POST'])
def classify():    
    if (request.data): 
        url = request.data
        result = classify_image(url)        
        print('Model classification: ' + result)        
        return result

@app.route('/api-astar-find-path', methods=['POST'])
def astar_pathfinding():    
    if (request.data): 
        grid = json.loads(request.data)
        result, grid_history = find_path(grid, node_config)
        
        if result == 0:
            return { "status" : "no start node"}
        elif result == 1:
            return { "status" : "no finish node"}
        

        grid_history_object = []
        for step in grid_history:
            grid_history_object.append(
                [[{"row" : node.row, "col" : node.col, "nodeType" : node.node_type, "fCost" : node.f_cost} for node in row] for row in step]
            )

        if result == 2:
            return { "status" : "blocked", "path" : None, "gridHistory" : grid_history_object }

        return_path = []
        for node in result:
            return_path.append({'row' : node.row, 'col' : node.col})

        return { "status" : "success", "path" : return_path, "gridHistory" : grid_history_object }

@app.route('/api-populate-grid', methods=['POST'])
def populate_grid():    
    if (request.data):     
        data = json.loads(request.data)
        grid = create_grid(node_config, *data.values())
        grid = [[{'row' : node.row, 'col' : node.col, 'nodeType' : node.node_type} for node in row] for row in grid]
        return {'grid' : grid}

@app.route('/api-generate-clusters', methods=['POST'])
def generate_clusters():
    if (request.data):
        data = json.loads(request.data)
        points = create_clusters(**data)
        return json.dumps([{"x": point[0], "y" : point[1] } for point in points])

@app.route('/api-knearest', methods=['POST'])
def apply_knearest():
    if (request.data):
        data = json.loads(request.data)
        points = np.array([list(point.values()) for point in data['points']])
        centers = data['nClusters'] 

        runs = knearest(points, centers=centers)
        best_run = min(runs, key=lambda x: x['cost'])        

        point_marker_size = 100
        classifier_marker_size = 200
        
        points = [{ 'x' : point[0], 'y' : point[1], 'classifier' : int(point[2]), 'distance' : point[3] } for point in best_run['points']]
        
        iteration_tracker = [   { 'points' :    [   
                                                    {   'x' : point[0], 
                                                        'y' : point[1],
                                                        'z' : point_marker_size, 
                                                        'classifier' : int(point[2]), 
                                                        'distance' : point[3] 
                                                    } for point in iteration[0]
                                                ],
                                'classifiers' : [   
                                                    {   'x' : classifier[0],
                                                        'y' : classifier[1], 
                                                        'z' : classifier_marker_size, 
                                                        'x_mass' : classifier[2], 
                                                        'y_mass' : classifier[3]
                                                    } for classifier in iteration[1]
                                                ]
                                } for iteration in best_run['iteration_tracker']
                            ]

        return_object = { 'points' : points, 'iteration_tracker' : iteration_tracker}

        return json.dumps(return_object)
        