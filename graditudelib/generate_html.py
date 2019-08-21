import os
from jinja2 import Template
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool


def generate_html_page(html_folder, html_folder_gene, html_folder_protein, rna_seq_file, protein_file):
    # html_folder = "../output"
    # html_folder_gene = "../output/gene"
    # html_folder_protein = "../output/protein"
    image_folder_gene = "{}/images".format(html_folder_gene)
    image_folder_protein = "{}/images".format(html_folder_protein)
    # rna_seq_file = "../input/scaled_Nor_gene_wise_100_to_max.csv"
    # protein_file = "../input/<Grad-seq_MS_for_Spearman>.csv"
    rna_seq_data = pd.read_csv(rna_seq_file, sep="\t")
    protein_data = pd.read_csv(protein_file, sep="\t")
    for folder in [html_folder, html_folder_gene, html_folder_protein, image_folder_gene, image_folder_protein]:
        if not os.path.exists(folder):
            os.mkdir(folder)
    generate_index_pager(rna_seq_data, protein_data, html_folder)
    generate_gene_pages(rna_seq_data, html_folder_gene, image_folder_gene)
    generate_protein_pages(protein_data, html_folder_protein, image_folder_protein)


def generate_index_pager(rna_seq_data, protein_data, html_folder):
    # template = Template(open("templates/gene_index_template.html").read())
    template = Template(open(
        "../templates/gene_index_template_bootstrap.html").read())
    gene_index_html = template.render(rna_seq_data=rna_seq_data, protein_data=protein_data)
    with open("{}/index.html".format(html_folder), "w") as output_fh:
        output_fh.write(gene_index_html)


def generate_gene_pages(rna_seq_data, html_folder_gene, image_folder):
    for index, row in rna_seq_data.iterrows():
        generate_gene_page(row, html_folder_gene, image_folder)
        generate_gene_rna_distri_image(row, image_folder)
        # exit(0)


def generate_protein_pages(protein_data, html_folder_protein, image_folder):
    for index, row in protein_data.iterrows():
        generate_protein_page(row, html_folder_protein, image_folder)
        generate_protein_distri_image(row, image_folder)
        # exit(0)


def generate_gene_page(row, html_folder, image_folder):
    locus_tag = row["Gene"]
    with open("{}/{}.html".format(html_folder, locus_tag),
              "w") as output_fh:
        # template = Template(open("templates/gene_template.html").read())
        template = Template(open("../templates/gene_template_bootstrap.html").read())
        gene_html = template.render(row=row)
        output_fh.write(gene_html.format(image_folder, locus_tag))


def generate_protein_page(row, html_folder, image_folder):
    locus_tag = row["Gene"]
    with open("{}/{}.html".format(html_folder, locus_tag),
              "w") as output_fh:
        # template = Template(open("templates/gene_template.html").read())
        template = Template(open("../templates/protein_template_bootstrap.html").read())
        gene_html = template.render(row=row)
        output_fh.write(gene_html.format(image_folder, locus_tag))


def generate_gene_rna_distri_image(row, image_folder):
    locus_tag = row["Gene"]
    counting_value_list = row.iloc[12:]
    plot_html = figure(title=locus_tag, plot_width=600, plot_height=600,
                       x_axis_label='Fraction number',
                       y_axis_label='Normalized and scaled to max read counts',
                       tools=[BoxZoomTool(), ResetTool(), PanTool(),
                              WheelZoomTool()])
    plot_html.yaxis.axis_label_text_font_size = "15pt"
    plot_html.xaxis.axis_label_text_font_size = "15pt"
    plot_html.title.text_font_size = '15pt'
    plot_html.toolbar.logo = None
    y_axis = range(1, 21)
    plot_html.line(y_axis, counting_value_list)
    output_file("{}/{}.html".format(image_folder, locus_tag))
    save(plot_html)


def generate_protein_distri_image(row, image_folder):
    locus_tag = row["Gene"]
    counting_value_list = row.iloc[8:28]
    plot_html = figure(title=locus_tag, plot_width=600, plot_height=600,
                       x_axis_label='Fraction number',
                       y_axis_label='Normalized and scaled to max read counts',
                       tools=[BoxZoomTool(), ResetTool(), PanTool(),
                              WheelZoomTool()])
    plot_html.yaxis.axis_label_text_font_size = "15pt"
    plot_html.xaxis.axis_label_text_font_size = "15pt"
    plot_html.title.text_font_size = '15pt'
    plot_html.toolbar.logo = None
    y_axis = range(1, 21)
    plot_html.line(y_axis, counting_value_list)
    output_file("{}/{}.html".format(image_folder, locus_tag))
    save(plot_html)

