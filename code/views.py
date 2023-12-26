#views.py
from flask import abort, jsonify, send_from_directory, render_template, request, redirect, url_for, send_file, make_response

from app import app
from models import *

import os
import csv
import json
import uuid
import pandas as pd
import requests
import requests_cache
import metadata_validator
import config
import pandas as pd
import ast

import config
from ccmsproteosafepythonapi import proteosafe
from ontology_utils import resolve_ontology

requests_cache.install_cache('./temp/requests_cache', allowable_codes=(200, 404, 500))


def count_compounds_in_files(filelist1, filelist2, filelist3, filelist4, filelist5, filelist6):
    output_list = []
    input_fileset1 = set(filelist1)
    input_fileset2 = set(filelist2)
    input_fileset3 = set(filelist3)
    input_fileset4 = set(filelist4)
    input_fileset5 = set(filelist5)
    input_fileset6 = set(filelist6)

    all_compounds = Compound.select()
    for my_compound in all_compounds:
        my_files = Filename.select().join(CompoundFilenameConnection).where(CompoundFilenameConnection.compound==my_compound)

        my_files_set = set([one_file.filepath for one_file in my_files])
        intersection_set1 = input_fileset1.intersection(my_files_set)
        intersection_set2 = input_fileset2.intersection(my_files_set)
        intersection_set3 = input_fileset3.intersection(my_files_set)
        intersection_set4 = input_fileset4.intersection(my_files_set)
        intersection_set5 = input_fileset5.intersection(my_files_set)
        intersection_set6 = input_fileset6.intersection(my_files_set)

        output_dict = {}
        output_dict["compound"] = my_compound.compoundname

        include_row = False

        output_dict["count1"] = len(intersection_set1)
        if len(filelist1) > 0:
            output_dict["count1_norm"] = int(float(len(intersection_set1)) / float(len(filelist1)) * 100.0)
        else:
            output_dict["count1_norm"] = 0

        output_dict["count2"] = len(intersection_set2)
        if len(filelist2) > 0:
            output_dict["count2_norm"] = int(float(len(intersection_set2)) / float(len(filelist2)) * 100.0)
        else:
            output_dict["count2_norm"] = 0

        output_dict["count3"] = len(intersection_set3)
        if len(filelist3) > 0:
            output_dict["count3_norm"] = int(float(len(intersection_set3)) / float(len(filelist3)) * 100.0)
        else:
            output_dict["count3_norm"] = 0

        output_dict["count4"] = len(intersection_set4)
        if len(filelist4) > 0:
            output_dict["count4_norm"] = int(float(len(intersection_set4)) / float(len(filelist4)) * 100.0)
        else:
            output_dict["count4_norm"] = 0

        output_dict["count5"] = len(intersection_set5)
        if len(filelist5) > 0:
            output_dict["count5_norm"] = int(float(len(intersection_set5)) / float(len(filelist5)) * 100.0)
        else:
            output_dict["count5_norm"] = 0

        output_dict["count6"] = len(intersection_set6)
        if len(filelist6) > 0:
            output_dict["count6_norm"] = int(float(len(intersection_set6)) / float(len(filelist6)) * 100.0)
        else:
            output_dict["count6_norm"] = 0

        counts_total = output_dict["count1"] + output_dict["count2"] + output_dict["count3"] + output_dict["count4"] + output_dict["count5"] + output_dict["count6"]
        if counts_total > 0:
            output_list.append(output_dict)

    return output_list

def count_tags_in_files(filelist1, filelist2, filelist3, filelist4, filelist5, filelist6):
    output_list = []
    input_fileset1 = set(filelist1)
    input_fileset2 = set(filelist2)
    input_fileset3 = set(filelist3)
    input_fileset4 = set(filelist4)
    input_fileset5 = set(filelist5)
    input_fileset6 = set(filelist6)

    all_tags = CompoundTag.select()
    for my_tag in all_tags:
        my_files = Filename.select().join(CompoundTagFilenameConnection).where(CompoundTagFilenameConnection.compoundtag==my_tag)

        my_files_set = set([one_file.filepath for one_file in my_files])
        intersection_set1 = input_fileset1.intersection(my_files_set)
        intersection_set2 = input_fileset2.intersection(my_files_set)
        intersection_set3 = input_fileset3.intersection(my_files_set)
        intersection_set4 = input_fileset4.intersection(my_files_set)
        intersection_set5 = input_fileset5.intersection(my_files_set)
        intersection_set6 = input_fileset6.intersection(my_files_set)

        output_dict = {}
        output_dict["compound"] = my_tag.tagname

        include_row = False

        output_dict["count1"] = len(intersection_set1)
        if len(filelist1) > 0:
            output_dict["count1_norm"] = int(float(len(intersection_set1)) / float(len(filelist1)) * 100.0)
        else:
            output_dict["count1_norm"] = 0

        output_dict["count2"] = len(intersection_set2)
        if len(filelist2) > 0:
            output_dict["count2_norm"] = int(float(len(intersection_set2)) / float(len(filelist2)) * 100.0)
        else:
            output_dict["count2_norm"] = 0

        output_dict["count3"] = len(intersection_set3)
        if len(filelist3) > 0:
            output_dict["count3_norm"] = int(float(len(intersection_set3)) / float(len(filelist3)) * 100.0)
        else:
            output_dict["count3_norm"] = 0

        output_dict["count4"] = len(intersection_set4)
        if len(filelist4) > 0:
            output_dict["count4_norm"] = int(float(len(intersection_set4)) / float(len(filelist4)) * 100.0)
        else:
            output_dict["count4_norm"] = 0

        output_dict["count5"] = len(intersection_set5)
        if len(filelist5) > 0:
            output_dict["count5_norm"] = int(float(len(intersection_set5)) / float(len(filelist5)) * 100.0)
        else:
            output_dict["count5_norm"] = 0

        output_dict["count6"] = len(intersection_set6)
        if len(filelist6) > 0:
            output_dict["count6_norm"] = int(float(len(intersection_set6)) / float(len(filelist6)) * 100.0)
        else:
            output_dict["count6_norm"] = 0

        counts_total = output_dict["count1"] + output_dict["count2"] + output_dict["count3"] + output_dict["count4"] + output_dict["count5"] + output_dict["count6"]
        if counts_total > 0:
            output_list.append(output_dict)

    return output_list

@app.route('/filename', methods=['GET'])
def getfilename():
    query_filename = request.args["query"].replace("/spectrum/", "/ccms_peak/")
    expanded_attributes = request.args.get("expanded", "false")

    filepath_db = Filename.select().where(Filename.filepath == query_filename)

    if len(filepath_db) == 0:
        return "[]"

    all_connections = FilenameAttributeConnection.select().where(FilenameAttributeConnection.filename == filepath_db)
    resolved_terms = []
    for connection in all_connections:
        attribute_name = connection.attribute.categoryname
        attribute_term = connection.attributeterm.term
        resolved_term = resolve_ontology(attribute_name, attribute_term)

        if expanded_attributes == "false" and attribute_name:
            resolved_terms.append(resolved_term)

        if expanded_attributes == "true" and not(attribute_name):
            resolved_terms.append(resolved_term)

    return json.dumps(resolved_terms)

@app.route('/filenamedict', methods=['GET'])
def queryfilename():
    query_filename = request.args["query"].replace("/spectrum/", "/ccms_peak/")
    expanded_attributes = request.args.get("expanded", "false")
    all_attributes = request.args.get("allattributes", "false")

    filepath_db = Filename.select().where(Filename.filepath == query_filename)

    if len(filepath_db) == 0:
        return "[]"

    all_connections = FilenameAttributeConnection.select().where(FilenameAttributeConnection.filename == filepath_db)
    resolved_terms = []
    for connection in all_connections:
        attribute_name = connection.attribute.categoryname
        attribute_term = connection.attributeterm.term
        resolved_term = resolve_ontology(attribute_name, attribute_term)

        if all_attributes == "true":
            resolved_terms.append({"attribute_name": attribute_name, "attribute_term" : resolved_term})
        else:
            if expanded_attributes == "false" and attribute_name:
                resolved_terms.append({"attribute_name": attribute_name, "attribute_term" : resolved_term})

            if expanded_attributes == "true" and not(attribute_name):
                resolved_terms.append({"attribute_name": attribute_name, "attribute_term" : resolved_term})

    return json.dumps(resolved_terms)


#Summarize Files Per Comparison Group
@app.route('/explorer', methods=['POST'])
def summarizefiles():
    all_files_G1 = json.loads(request.values.get("G1", "[]"))
    all_files_G2 = json.loads(request.values.get("G2", "[]"))
    all_files_G3 = json.loads(request.values.get("G3", "[]"))
    all_files_G4 = json.loads(request.values.get("G4", "[]"))
    all_files_G5 = json.loads(request.values.get("G5", "[]"))
    all_files_G6 = json.loads(request.values.get("G6", "[]"))

    output = count_compounds_in_files(all_files_G1, all_files_G2, all_files_G3, all_files_G4, all_files_G5, all_files_G6)

    return json.dumps(output)

# Lists all Compounds
@app.route('/compounds', methods=['GET'])
def querycompounds(): 
    file_list = []
    try:
        file_list = ast.literal_eval(request.args["files"])["filenames"]
    except:
        pass 
    all_compounds = []
    
    #in the case we display all compounds from all files
    if len(file_list) == 0:
        all_compounds_db = CompoundFilenameConnection.select(CompoundFilenameConnection.compound, fn.COUNT(CompoundFilenameConnection.compound).alias('count')).join(Compound).group_by(CompoundFilenameConnection.compound).dicts()
        for compound in all_compounds_db:
            compound_dict = {}
            compound_dict["compound"]= compound["compound"]
            compound_dict["count"] = compound["count"]
            all_compounds.append(compound_dict)
    
    #in the case of file filtration based on metadata
    else:
        all_compounds_db = CompoundFilenameConnection.select(CompoundFilenameConnection.compound, fn.COUNT(CompoundFilenameConnection.compound).alias('count')).where(CompoundFilenameConnection.filename.in_(file_list)).join(Compound).group_by(CompoundFilenameConnection.compound).dicts()
    
        for compound in all_compounds_db: 
            compound_dict = {}
            compound_dict["compound"] = compound["compound"]
            compound_dict["count"] = compound["count"]
            all_compounds.append(compound_dict)

    return json.dumps(all_compounds)

@app.route('/compoundfilename', methods=['GET'])
def queryfilesbycompound():
    compoundname = request.args['compoundname']
    compound_db = Compound.select().where(Compound.compoundname == compoundname)

    filenames_db = Filename.select().join(CompoundFilenameConnection).where(CompoundFilenameConnection.compound==compound_db)

    output_filenames = []
    for filename in filenames_db:
        output_filenames.append({"filepath" : filename.filepath})

    return json.dumps(output_filenames)

@app.route('/compoundenrichment', methods=['POST'])
def compoundenrichment():
    blacklist_attributes = ["ATTRIBUTE_DatasetAccession", "ATTRIBUTE_Curated_BodyPartOntologyIndex", "filename", "UniqueSubjectID", "UBERONOntologyIndex", "SubjectIdentifierAsRecorded", "SampleCollectionDateandTime", "LatitudeandLongitude", "InternalStandardsUsed", "DepthorAltitudeMeters", "DOIDOntologyIndex", "Country", "ComorbidityListDOIDIndex", "AgeInYears"]

    compoundname = request.form['compoundname']
    compound_db = Compound.select().where(Compound.compoundname == compoundname)

    compound_filenames = [filename.filepath for filename in Filename.select().join(CompoundFilenameConnection).where(CompoundFilenameConnection.compound==compound_db)]

    
    enrichment_list = []

    if "filenames" in request.form:
        filter_filenames = set(json.loads(request.form["filenames"]))
        if len(filter_filenames) == 0:
            filter_filenames = set([filename.filepath for filename in Filename.select()])
    else:
        filter_filenames = set([filename.filepath for filename in Filename.select()])

    all_metadata = FilenameAttributeConnection.select(Attribute.categoryname, AttributeTerm.term, fn.COUNT(FilenameAttributeConnection.filename).alias('ct')).join(Attribute).switch(FilenameAttributeConnection).join(AttributeTerm).group_by(Attribute.categoryname, AttributeTerm.term).dicts()    
     
    for attribute_term_pair in all_metadata:
        # if attribute_term_pair["categoryname"].find("ATTRIBUTE_") == -1:
        #    continue

        if attribute_term_pair["categoryname"] in blacklist_attributes:
            continue
        
        
        attribute_files_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == attribute_term_pair["term"]).where(FilenameAttributeConnection.attribute == attribute_term_pair["categoryname"])
        attribute_filenames = set([filename.filepath for filename in attribute_files_db]).intersection(filter_filenames)
        
        if len(attribute_filenames) > 0:
            intersection_filenames = set(compound_filenames).intersection(set(attribute_filenames)).intersection(filter_filenames)

            enrichment_dict = {}
            enrichment_dict["attribute_name"] = attribute_term_pair["categoryname"]
            enrichment_dict["attribute_term"] = attribute_term_pair["term"]
            enrichment_dict["totalfiles"] = len(attribute_filenames)
            enrichment_dict["compoundfiles"] = len(intersection_filenames)
            enrichment_dict["percentage"] = len(intersection_filenames)/float(len(attribute_filenames))

            enrichment_list.append(enrichment_dict)

    enrichment_list = sorted(enrichment_list, key=lambda list_object: list_object["percentage"], reverse=True)

    # Creating Bokeh Plot Here
    enrichment_df = pd.DataFrame(enrichment_list)
    
    # Finding all non-zero entries
    enrichment_df = enrichment_df[enrichment_df["totalfiles"] != 0]
    all_attributes = list(set(list(enrichment_df["attribute_name"])))

    from bokeh.models import Panel, Tabs
    from bokeh.plotting import figure
    from bokeh.embed import components
    
    all_tabs = []

    for attribute in all_attributes:
        filtered_df = enrichment_df[enrichment_df["attribute_name"] == attribute]
        filtered_df = filtered_df[filtered_df["percentage"] > 0]

        all_terms = list(filtered_df["attribute_term"])
        all_percentage = list(filtered_df["percentage"])
        plot = figure(x_range=all_terms, plot_height=300, plot_width=1200, sizing_mode="scale_width", title="{} Percentage of Terms".format(attribute))
        plot.vbar(x=all_terms, top=all_percentage, width=0.9)
        tab = Panel(child=plot, title=attribute)

        all_tabs.append(tab)

    tabs = Tabs(tabs=all_tabs)
    script, div = components(tabs)

    drawing_dict = {}
    drawing_dict["div"] = div
    drawing_dict["script"] = script

    return_dict = {}
    return_dict["enrichment_list"] = enrichment_list
    return_dict["drawings"] = drawing_dict

    return json.dumps(return_dict)

@app.route('/filesenrichment', methods=['POST'])
def filesenrichment():
    blacklist_attributes = ["ATTRIBUTE_DatasetAccession", "ATTRIBUTE_Curated_BodyPartOntologyIndex"]

    compound_filenames = set(json.loads(request.form["filenames"]))
    enrichment_list = []
        
    filter_filenames = set([filename.filepath for filename in Filename.select()])

    all_metadata = FilenameAttributeConnection.select(Attribute.categoryname, AttributeTerm.term, fn.COUNT(FilenameAttributeConnection.filename).alias('ct')).join(Attribute).switch(FilenameAttributeConnection).join(AttributeTerm).group_by(Attribute.categoryname, AttributeTerm.term).dicts()

    for attribute_term_pair in all_metadata:
        if attribute_term_pair["categoryname"].find("ATTRIBUTE_") == -1:
            continue

        if attribute_term_pair["categoryname"] in blacklist_attributes:
            continue

        attribute_files_db = Filename.select().join(FilenameAttributeConnection).where(FilenameAttributeConnection.attributeterm == attribute_term_pair["term"]).where(FilenameAttributeConnection.attribute == attribute_term_pair["categoryname"])
        attribute_filenames = set([filename.filepath for filename in attribute_files_db]).intersection(filter_filenames)

        if len(attribute_filenames) > 0:
            intersection_filenames = set(compound_filenames).intersection(set(attribute_filenames)).intersection(filter_filenames)

            enrichment_dict = {}
            enrichment_dict["attribute_name"] = attribute_term_pair["categoryname"]
            enrichment_dict["attribute_term"] = attribute_term_pair["term"]
            enrichment_dict["totalfiles"] = len(attribute_filenames)
            enrichment_dict["compoundfiles"] = len(intersection_filenames)
            enrichment_dict["percentage"] = len(intersection_filenames)/float(len(attribute_filenames))

            enrichment_list.append(enrichment_dict)

    enrichment_list = sorted(enrichment_list, key=lambda list_object: list_object["percentage"], reverse=True)

    return json.dumps(enrichment_list)



@app.route('/tagexplorer', methods=['POST'])
def summarizetagfiles():
    all_files_G1 = json.loads(request.form["G1"])
    all_files_G2 = json.loads(request.form["G2"])
    all_files_G3 = json.loads(request.form["G3"])
    all_files_G4 = json.loads(request.form["G4"])
    all_files_G5 = json.loads(request.form["G5"])
    all_files_G6 = json.loads(request.form["G6"])

    output = count_tags_in_files(all_files_G1, all_files_G2, all_files_G3, all_files_G4, all_files_G5, all_files_G6)

    return json.dumps(output)

@app.route('/plottags', methods=['POST'])
def plottags():
    import os
    uuid_to_use = str(uuid.uuid4())
    input_filename = os.path.join("static", "temp", uuid_to_use + ".tsv")
    all_counts = json.loads(request.form["tagcounts"])
    sourcelevel = request.form["sourcelevel"]

    with open(input_filename, 'w') as csvfile:
        field_name = ["source information", "G1 number", "G1 percent", "G2 number", "G2 percent", "G3 number", "G3 percent", "G4 number", "G4 percent", "G5 number", "G5 percent", "G6 number", "G6 percent"]
        writer = csv.DictWriter(csvfile, fieldnames=field_name, delimiter="\t")

        writer.writeheader()

        for row in all_counts:
            new_dict = {}
            new_dict["source information"] = row["compound"]
            new_dict["G1 number"] = row["count1"]
            new_dict["G1 percent"] = row["count1_norm"]
            new_dict["G2 number"] = row["count2"]
            new_dict["G2 percent"] = row["count2_norm"]
            new_dict["G3 number"] = row["count3"]
            new_dict["G3 percent"] = row["count3_norm"]
            new_dict["G4 number"] = row["count4"]
            new_dict["G4 percent"] = row["count4_norm"]
            new_dict["G5 number"] = row["count5"]
            new_dict["G6 percent"] = row["count5_norm"]
            new_dict["G6 number"] = row["count6"]
            new_dict["G6 percent"] = row["count6_norm"]
            writer.writerow(new_dict)

    output_counts_png = os.path.join("static", "temp", uuid_to_use + "_count.png")
    output_percent_png = os.path.join("static", "temp", uuid_to_use + "_percent.png")

    cmd = "Rscript %s %s %s %s %s" % ("Meta_Analysis_Plot_Example.r", input_filename, output_counts_png, output_percent_png, sourcelevel)
    os.system(cmd)

    return json.dumps({"uuid" : uuid_to_use})


""" Production Views """

@app.route('/', methods=['GET'])
def homepage():
    total_files = Filename.select().count()
    total_identifications = CompoundFilenameConnection.select().count()
    total_compounds = Compound.select().count()
    return render_template('homepage.html', total_files=total_files, total_identifications=total_identifications, total_compounds=total_compounds)

@app.route('/globalmultivariate', methods=['GET'])
def globalmultivariate():
    return render_template('globalmultivariate.html')

@app.route('/comparemultivariate', methods=['GET', 'POST'])
def comparemultivariate():
    return render_template('comparemultivariate.html')

@app.route('/compoundslist', methods=['GET'])
def compoundslist():
    return render_template('compoundslist.html')

@app.route('/compoundfilenamelist', methods=['GET'])
def compoundfilenamelist():
    return render_template('compoundfilelist.html')

#Summarize Files Per Comparison Group
@app.route('/explorerdashboard', methods=['GET'])
def explorerdashboard():
    return render_template('explorerdashboard.html')

@app.route('/compoundenrichmentdashboard', methods=['GET'])
def compoundenrichmentview():
    return render_template('compoundenrichment.html')

@app.route('/metadataselection', methods=['GET'])
def metadataselection():
    return render_template('metadataselection.html')

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "{'status' : 'up'}"

@app.route('/datalookup', methods=['GET'])
def datalookup():
    return render_template('datalookup.html')

@app.route('/dump', methods=['GET'])
def dump():
    return send_file(config.PATH_TO_ORIGINAL_MAPPING_FILE, cache_timeout=1, as_attachment=True, attachment_filename="all_sampleinformation.tsv")

@app.route('/ReDUValidator', methods = ["GET"])
def ReDUValidator():
    return render_template('ReDUValidator.html')


# API End Points
@app.route('/metabatchdump', methods=['GET'])
def metabatchdump():
    df = pd.read_table(config.PATH_TO_ORIGINAL_MAPPING_FILE)
    filenames = df["filename"].tolist()
    batch_size = 1000
    batch_num = len(filenames) // batch_size
    output_list = []
    for x in range(batch_num):
        files = filenames[(batch_size * x):(batch_size * (x+1))]
        string_temp = ';'.join(files)
        output_dict = {}
        output_dict["filename"] = string_temp
        output_dict["id"] = x
        output_list.append(output_dict)

    new_file = pd.DataFrame(output_list)
    return new_file.to_csv(sep="\t", index=False)

def allowed_file_metadata(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ["tsv"]

@app.route('/validate', methods=['POST'])
def validate():
    request_file = request.files['file']
    #Invalid File Types
    if not allowed_file_metadata(request_file.filename):
        error_dict = {}
        error_dict["header"] = "Incorrect File Type"
        error_dict["line_number"] = "N/A"
        error_dict["error_string"] = "Please provide a tab separated file"

        validation_dict = {}
        validation_dict["status"] = False
        validation_dict["errors"] = [error_dict]
        validation_dict["stats"] = []
        validation_dict["stats"].append({"type":"total_rows", "value": 0})
        validation_dict["stats"].append({"type":"valid_rows", "value": 0})

        return json.dumps(validation_dict)
    
    
    local_filename = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
    request_file.save(local_filename)
     
    """Trying stuff out with pandas"""
    metadata_df = pd.read_csv(local_filename, sep="\t")
    metadata_df.to_csv(local_filename, index=False, sep="\t")

    metadata_validator.rewrite_metadata(local_filename)
    
    pass_validation, failures, errors_list, valid_rows, total_rows = metadata_validator.perform_validation(local_filename)

    validation_dict = {}
    validation_dict["status"] = pass_validation
    validation_dict["errors"] = errors_list
    validation_dict["stats"] = []

    validation_dict["stats"].append({"type":"total_rows", "value":total_rows})
    validation_dict["stats"].append({"type":"valid_rows", "value":len(valid_rows)})

    """Try to find datasets in public data"""
    try:
        dataset_success, result_string, valid_items = metadata_validator.perform_validation_against_massive(local_filename)
        validation_dict["stats"].append({"type":"massive_files_founds", "value": valid_items})

    except:
        print("Massive validation error")

    try:
        os.remove(local_filename)
    except:
        print("Cannot Remove File")

    return (json.dumps(validation_dict), {'Content-Type': 'application/json'})
