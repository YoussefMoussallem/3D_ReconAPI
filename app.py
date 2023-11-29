from flask import Flask, jsonify, request, send_file
from ReconMethods.Poisson_Recon import Poisson
from ReconMethods.Alpha import AlphaShape
from ReconMethods.BallPivoting import BPA
 
import open3d as o3d
import base64
import tempfile
from io import BytesIO

app = Flask(__name__)




@app.route('/Poisson', methods=['POST'])
def Poisson_Recon():
    if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

        # Save the file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ply')
    file.save(temp_file.name)

    normalestaradius = float(request.form.get('normalestaradius', 0.2))
    normalestamaxnn = int(request.form.get('normalestamaxnn', 40))
    outlier_neighbours = int(request.form.get('outlier_neighbours', 20))
    outlierstd_ratio = float(request.form.get('outlierstd_ratio', 2))
    depth = int(request.form.get('unique_param', 9))

    poisson=Poisson(temp_file.name)
    poisson.CreateModel(depth,normalestaradius,normalestamaxnn,outlier_neighbours,outlierstd_ratio) #8,0.03,100,20,2
    poisson.save("Results/Server_Output.ply")
    return send_file("Results/Server_Output.ply", as_attachment=True)


@app.route('/AlphaShape', methods=['POST'])
def Alpha():
    if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

        # Save the file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ply')
    file.save(temp_file.name)

    normalestaradius = float(request.form.get('normalestaradius', 0.03))
    normalestamaxnn = int(request.form.get('normalestamaxnn', 100))
    outlier_neighbours = int(request.form.get('outlier_neighbours', 20))
    outlierstd_ratio = float(request.form.get('outlierstd_ratio', 2))
    alpha = float(request.form.get('unique_param', 0.005))

    alphashape=AlphaShape(temp_file.name)
    alphashape.CreateModel(alpha,normalestaradius,normalestamaxnn,outlier_neighbours,outlierstd_ratio)  #0.09,0.03,100,20,2
    alphashape.save("Results/Server_Output.ply")
    return send_file("Results/Server_Output.ply", as_attachment=True)




#TO BE FIXED(NOT WORKING)
@app.route('/BPA', methods=['POST'])
def BallPivoting():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

        # Save the file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ply')
    file.save(temp_file.name)

    bpa=BPA(temp_file.name)
    bpa.CreateModel(0.5)
    bpa.save("Results/Server_Output.ply")
    return send_file("Results/Server_Output.ply", as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
