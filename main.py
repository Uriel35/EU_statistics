import re

import matplotlib
matplotlib.use('TkAgg')  # Cambiar el backend a TkAgg
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from utils import colors_util as colors, fx_utils as fx_utils
import json


def get_promedio_especialidad(data_path, especialidad, resto, puntaje_final):
    df = pd.read_csv(data_path)
    filtro = df['Especialidad'] == especialidad
    df = df[filtro]

    if puntaje_final:
        df = df.sort_values(by="Puntaje final", ascending=False)
        if resto == 1:
            return df.iloc[-1]['Puntaje final']
        return df.iloc[-resto - 1]['Puntaje final']
    else:
        df = df.sort_values(by="Promedio", ascending=False)
        if resto == 1:
            return df.iloc[-1]['Promedio']
        return df.iloc[-resto - 1]['Promedio']


def vacancies_applicants_chart(desertion_path, data_path, puntaje_final):
    df = pd.read_csv(desertion_path)
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Postulantes", ascending=False)

    ## Para seleccionar parte 1, parte 2 y parte 3
    # df = df[0:15]
    df = df[15: 30]
    # df = df[30:]
    max_applicants = df['Postulantes'].max()

    for especialidad in df.index:
        cupos = df.loc[especialidad]['Cupos']
        resto = df.loc[especialidad]['Resto']
        postulantes = df.loc[especialidad]['Postulantes']
        especialidad_label = fx_utils.replace_speciality_names(especialidad)
        if resto > 0:
            plt.bar(especialidad_label, [cupos], color=colors.celeste)
            plt.bar(especialidad_label, [resto], bottom=cupos, color=colors.rojo)
            promedio = get_promedio_especialidad(especialidad=especialidad, resto=resto, data_path=data_path, puntaje_final=puntaje_final)
            plt.text(especialidad_label, cupos + (max_applicants * 0.06), str(promedio), ha='center', va='top')
            # plt.text(especialidad_label, postulantes, str(promedio), ha='center', va='top')
        elif resto < 0:
            plt.bar(especialidad_label, [postulantes], color=colors.celeste)
            plt.bar(especialidad_label, [resto * (-1)], bottom=postulantes, color=colors.verde)
        else:
            plt.bar(especialidad_label, [postulantes], color=colors.celeste)

    referencias = [plt.Rectangle((0, 0), 1, 1, color=colors.celeste),
                   plt.Rectangle((0, 0), 1, 1, color=colors.rojo),
                   plt.Rectangle((0, 0), 1, 1, color=colors.verde)]
    plt.legend(referencias, ['Cupos tomados', 'Postulantes sin cupo', 'Cupos sobrantes'])
    plt.tick_params(axis='x', labelrotation=45)
    if puntaje_final:
        plt.title('Habilitados y Cupos (Puntajes finales limites en postulantes sin cupo)')
    else:
        plt.title('Habilitados y Cupos (promedios limites en postulantes sin cupo)')
    plt.xlabel('Especialidad')
    plt.ylabel('Postulantes, Cupos')
    plt.show()


def desertion_chart(desertion_path):
    desercion_df = pd.read_csv(desertion_path)
    resto_filter = desercion_df['Resto'] > 0
    desercion_df = desercion_df[resto_filter].sort_values(by='Resto', ascending=False)
    desercion_df['Especialidad'] = desercion_df['Especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    desercion_df = desercion_df[0:20]

    plt.bar(desercion_df['Especialidad'], desercion_df['Resto'], color=colors.rojo)
    for i, valor in enumerate(desercion_df['Resto']):
        plt.annotate(str(valor), xy=(i, valor), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=10)
    plt.tick_params(axis='x', labelrotation=45, labelsize=8)
    plt.suptitle('Postulantes sin cupo segun especialidad')
    total_desertion = desercion_df[desercion_df['Resto'] > 0 ]['Resto'].sum()
    plt.title(f'({total_desertion} postulantes totales sin cupo)', fontsize=10)
    plt.xlabel('Especialidad')
    plt.ylabel('Postulantes sin cupos')
    plt.show()


def free_vacancies_chart(desertion_path):
    desercion_df = pd.read_csv(desertion_path)
    desercion_df['Especialidad'] = desercion_df['Especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    filter = desercion_df['Resto'] < 0
    desercion_df['Resto'] = desercion_df['Resto'].apply(lambda x: x * -1)
    desercion_df = desercion_df[filter].sort_values(by='Resto', ascending=False)
    total = desercion_df['Resto'].sum()
    plt.bar(desercion_df['Especialidad'], desercion_df['Resto'], color=colors.verde)
    for i, valor in enumerate(desercion_df['Resto']):
        plt.annotate(str(valor), xy=(i, valor), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=10)
    plt.tick_params(axis='x', labelrotation=45, labelsize=8)
    plt.suptitle('Cupos libres segun especialidad', fontsize=13)
    plt.title(f'({total} cupos libres en total)', fontsize=9)
    plt.xlabel('Especialidad')
    plt.ylabel('Cupos libres')
    plt.show()


def score_variation_by_speciality_chart(data_path):
    score_df = pd.read_csv(data_path)
    score_df['Especialidad'] = score_df['Especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    medians = score_df.groupby('Especialidad')['Promedio'].median()
    score_df['median'] = score_df['Especialidad'].map(medians)
    score_df = score_df.sort_values('median')

    unique_specialities = list(score_df['Especialidad'].unique())
    p1 = unique_specialities[:int(len(unique_specialities) / 2)]
    p2 = unique_specialities[int(len(unique_specialities) / 2):]

    for i, parte in enumerate([p1, p2]):
        grupo = score_df[score_df['Especialidad'].isin(parte)]

        sns.boxplot(x='Especialidad', y='Promedio', data=grupo)

        plt.xlabel('Especialidad')
        plt.ylabel('Promedio')
        plt.suptitle('Distribución del promedio por especialidad', fontsize=15)
        plt.tick_params(axis='x', labelrotation=45, labelsize=8)

        # plt.savefig(f'./images/score/score_box_chart_p{i + 1}.png', dpi=300)
        plt.show()


def score_chart(data_path):
    score_df = pd.read_csv(data_path)
    score_df = score_df.dropna(how='all')
    score_df = score_df.sort_values('Promedio')

    ## Media total
    media = score_df['Promedio'].mean()

    conteo = score_df['Promedio'].dropna()

    ## Redondear por 0.25
    # conteo = conteo.apply(lambda x: round(x * 4) / 4)
    ## Redondear por 0.2
    conteo = conteo.apply(lambda x: round(x * 5) / 5)
    ## Redondear por 0.1
    # conteo = conteo.apply(lambda x: round(x * 10) / 10)

    conteo = conteo.value_counts().sort_index()

    plt.plot(conteo.index, conteo.values, color=colors.celeste)
    plt.scatter(conteo.index, conteo.values, color=colors.celeste)
    plt.xlabel('Promedios')
    plt.ylabel('Cantidad')
    plt.suptitle('Distribucion de promedios general', fontsize=13)
    plt.title(f'(Media de {round(media, 2)})', fontsize=9)
    plt.show()


def applicants_pie_chart(desertion_path):
    df = pd.read_csv(desertion_path)
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Postulantes", ascending=False)

    threshold = 1.5
    total = sum(df['Postulantes'])
    df['Porcentaje'] = df['Postulantes'].apply(lambda x: round((x / total) * 100, 1))
    others_df = df[df['Porcentaje'] < threshold]
    upper_df = df[df['Porcentaje'] > threshold]
    others_for_pie_df = others_df.sum().T
    others_for_pie_df.name = f'Otros (< {threshold}%)'
    upper_df = upper_df._append(others_for_pie_df)
    plt.pie(upper_df['Porcentaje'], labels=[fx_utils.replace_speciality_names(label) for label in upper_df.index], autopct='%1.1f%%', startangle=90, colors=[colors.speciality_colors.get(i, 'gray') for i in upper_df.index])
    plt.title('% Postulantes a especialidad', fontsize=13)
    # plt.savefig('./images/applicants/applicants_pie.png')
    plt.show()


def vacancies_pie_chart(desertion_path):
    df = pd.read_csv(desertion_path)
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Cupos", ascending=False)

    threshold = 1.2
    total = sum(df['Cupos'])
    df['Porcentaje'] = df['Cupos'].apply(lambda x: round((x / total) * 100, 1))
    others_df = df[df['Porcentaje'] < threshold]
    upper_df = df[df['Porcentaje'] > threshold]
    others_for_pie_df = others_df.sum().T
    others_for_pie_df.name = f'Otros (< {threshold}%)'
    upper_df = upper_df._append(others_for_pie_df)

    plt.pie(upper_df['Porcentaje'], labels=[fx_utils.replace_speciality_names(label) for label in upper_df.index], autopct='%1.1f%%', startangle=90, colors=[colors.speciality_colors.get(i, 'gray') for i in upper_df.index])
    plt.title('% Cupos oficiales por especialidad', fontsize=13)
    # plt.savefig('./images/vacancies/vacancies_pie.png')
    plt.show()


### Ejecutar los diferentes plots
desercion_2022 = 'data/2022/desercion_2022.csv'
data_2022 = 'data/2022/anon_data_2022.csv'
desercion_2023 = 'data/2023/desercion_2023.csv'
data_2023 = 'data/2023/anon_data_2023.csv'

# vacancies_applicants_chart(desertion_path=desercion_2022, data_path=data_2022, puntaje_final=True)
# desertion_chart(desertion_path=desercion_2022)
# free_vacancies_chart(desertion_path=desercion_2022)
score_variation_by_speciality_chart(data_path=data_2022)
# score_chart(data_path=data_2022)
# applicants_pie_chart(desertion_path=desercion_2022)
# vacancies_pie_chart(desertion_path=desercion_2023)
# vacancies_pie_chart(desertion_path=desercion_2022)
