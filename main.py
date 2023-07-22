import re
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils import colors_util as colors, fx_utils as fx_utils
import numpy as np


def vacancies_applicants_chart(desertion_path, data_path, puntaje="Promedio"):
    def get_limit(data_path, especialidad, resto, puntaje):
        data_df = pd.read_csv(data_path)
        data_df[puntaje] = data_df[puntaje].fillna(0)
        data_df = data_df[data_df['Especialidad'] == especialidad]
        data_df = data_df.sort_values(by=puntaje, ascending=False)
        if resto == 1:
            return data_df.iloc[-1][puntaje]
        return data_df.iloc[-resto - 1][puntaje]

    df = pd.read_csv(desertion_path)
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Postulantes", ascending=False)

    for df_fragment in [df[0:15], df[15:30], df[30:]]:
        print(df_fragment)
        max_applicants = df_fragment['Postulantes'].max()
        fig, ax = plt.subplots()
        for especialidad in df_fragment.index:
            cupos = df_fragment.loc[especialidad]['Cupos']
            resto = df_fragment.loc[especialidad]['Resto']
            postulantes = df_fragment.loc[especialidad]['Postulantes']
            especialidad_label = fx_utils.replace_speciality_names(especialidad)
            if resto > 0:
                ax.bar(especialidad_label, [cupos], color=colors.celeste)
                ax.bar(especialidad_label, [resto], bottom=cupos, color=colors.rojo)
                limit = get_limit(especialidad=especialidad, resto=resto, data_path=data_path, puntaje=puntaje)
                plt.text(especialidad_label, cupos + (max_applicants * 0.06), str(limit), ha='center', va='top')
            elif resto < 0:
                ax.bar(especialidad_label, [postulantes], color=colors.celeste)
                ax.bar(especialidad_label, [resto * (-1)], bottom=postulantes, color=colors.verde)
            else:
                ax.bar(especialidad_label, [postulantes], color=colors.celeste)

        referencias = [plt.Rectangle((0, 0), 1, 1, color=colors.celeste),
                       plt.Rectangle((0, 0), 1, 1, color=colors.rojo),
                       plt.Rectangle((0, 0), 1, 1, color=colors.verde)]
        ax.locator_params(axis='y', integer=True)
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.locator_params(axis='y', integer=True)

        plt.legend(referencias, ['Cupos tomados', 'Postulantes sin cupo', 'Cupos sobrantes'])
        ax.tick_params(axis='x', labelrotation=45)
        plt.title(f'Habilitados y Cupos, ({puntaje} limites en postulantes sin cupo)')
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


def score_variation_by_speciality_chart(data_path, puntaje="Promedio"):
    score_df = pd.read_csv(data_path)
    score_df['Especialidad'] = score_df['Especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    medians = score_df.groupby('Especialidad')[puntaje].median()
    score_df['median'] = score_df['Especialidad'].map(medians)
    score_df = score_df.sort_values('median')

    unique_specialities = list(score_df['Especialidad'].unique())
    p1 = unique_specialities[:int(len(unique_specialities) / 2)]
    p2 = unique_specialities[int(len(unique_specialities) / 2):]

    for i, parte in enumerate([p1, p2]):
        grupo = score_df[score_df['Especialidad'].isin(parte)]
        grupo = grupo[grupo['Promedio'] != 0]

        fig, ax = plt.subplots()
        sns.boxplot(x='Especialidad', y=puntaje, data=grupo, ax=ax)
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())

        plt.xlabel('Especialidad')
        plt.ylabel(puntaje)
        plt.suptitle(f'Distribución del {puntaje} por especialidad', fontsize=15)
        ax.tick_params(axis='x', labelrotation=45, labelsize=8)

        # plt.savefig(f'./images/score/score_box_chart_p{i + 1}.png', dpi=300)
        plt.show()


def score_chart(data_paths, years, puntaje='Promedio', interval=0.2):
    fig, ax = plt.subplots()
    colores = list(colors.speciality_colors.values())[:len(years)]
    for year, paths, color in zip(years, data_paths, colores):
        score_df = pd.read_csv(paths)
        score_df = score_df.dropna(how='all')
        score_df = score_df.sort_values(puntaje)

        media = score_df[puntaje].mean()

        conteo = score_df[puntaje].dropna()
        divisor = 10 / (10 * interval)
        conteo = conteo.apply(lambda x: round(x * divisor) / divisor)

        conteo = conteo.value_counts().sort_index()
        if 0 in conteo.index:
            conteo = conteo.drop(0)

        ax.plot(conteo.index, conteo.values, color=color, label=year)
        # ax.scatter(media, [50], color='red', label=f'Media {year}')

    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax.set_ylabel('Cantidad')
    ax2.set_ylabel('Cantidad')
    ax.set_xlabel(puntaje)
    ax.legend()
    plt.suptitle(f'Distribucion de {puntaje} general', fontsize=13)
    # plt.title(f'(Media de {round(media, 2)})', fontsize=9)

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


def all_years_score_chart(desertion_paths, interval, puntaje):
    fig, ax = plt.subplots()
    colors_list = list(colors.speciality_colors.values())
    referencias = {}

    for path in desertion_paths:
        df = pd.read_csv(path)
        df[puntaje] = df[puntaje].dropna()
        df = df[df[puntaje] != 0]

        divisor = 10 / (10 * interval)
        conteo = df[puntaje].dropna().apply(lambda x: round(x * divisor) / divisor)
        conteo = conteo.value_counts().sort_index()

        ax.plot(conteo.index, conteo.values, color=colors_list[0])
        ax.scatter(conteo.index, conteo.values, color=colors_list[0])
        referencias[re.search('\d{1,4}', path).group()] = plt.Rectangle((0, 0), 1, 1, color=colors_list[0])
        colors_list = colors_list[1:]

    plt.suptitle(f'Distribucion de {puntaje} general', fontsize=13)
    plt.title(f'Redondeados por un intervalo de {interval}', fontsize=10)
    ax.set_ylabel('Cantidad')
    ax.set_xlabel(puntaje)
    plt.legend(referencias.values(), referencias.keys())
    plt.show()


def make_reincidence_bar_plot(reincidence_path):
    reincidence_df = pd.read_csv(reincidence_path)

    especialidad = reincidence_df['Especialidad_vieja_22'].value_counts()
    nueva_especialidad = reincidence_df['Especialidad_23'].value_counts()

    reincidence_df = pd.concat([especialidad, nueva_especialidad], axis=1, keys=[especialidad.index.name, nueva_especialidad.index.name])

    ## Para que sea mas lindo, acorte hasta el 15... Hay muchas mas pero de poca cantidad
    reincidence_df = reincidence_df[:15]

    bar_width = 0.35
    fix, ax = plt.subplots()
    pos1 = np.arange(len(reincidence_df.index))
    pos2 = pos1 + bar_width
    ax.bar(pos1, reincidence_df['Especialidad_vieja_22'], bar_width, label='Especialidad anterior')
    ax.bar(pos2, reincidence_df['Especialidad_23'], bar_width, label='Especialidad actual')
    ax.legend()
    ax.set_xlabel('Especialidad')
    ax.set_ylabel('Cantidad de personas')
    ax.set_xticks(pos1 + bar_width / 2)
    ax.set_xticklabels(reincidence_df.index)
    ax.tick_params(axis='x', labelrotation=45)
    plt.title('Reincidencia entre años 2022-2023')
    plt.show()


### Ejecutar los diferentes plots
desercion_2022 = 'data/2022/desercion_2022.csv'
data_2022 = 'data/2022/anon_data_2022.csv'
desercion_2023 = 'data/2023/desercion_2023.csv'
data_2023 = 'data/2023/anon_data_2023.csv'
reincidencia_2023 = 'data/2023/anon_reincidencia_2023.csv'

# all_years_score_chart([data_2022, data_2023], interval=0.2, puntaje='Promedio')

# vacancies_applicants_chart(desertion_path=desercion_2022, data_path=data_2022, puntaje='Puntaje final')
# desertion_chart(desertion_path=desercion_2022)
# free_vacancies_chart(desertion_path=desercion_2022)
# score_variation_by_speciality_chart(data_path=data_2022, puntaje='Examen')
# score_variation_by_speciality_chart(data_path=data_2022, puntaje='Puntaje final')
# score_variation_by_speciality_chart(data_path=data_2022, puntaje='Promedio')
# score_chart(data_path=data_2022, puntaje='Examen', interval=1)
# score_chart(data_path=data_2022, puntaje='Puntaje final', interval=1)
# score_chart(data_path=data_2022, puntaje='Promedio', interval=0.2)
# applicants_pie_chart(desertion_path=desercion_2022)
# vacancies_pie_chart(desertion_path=desercion_2022)

# vacancies_applicants_chart(desertion_path=desercion_2023, data_path=data_2023, puntaje='Promedio')
# vacancies_applicants_chart(desertion_path=desercion_2023, data_path=data_2023, puntaje='Puntaje final')
# desertion_chart(desertion_path=desercion_2023)
# free_vacancies_chart(desertion_path=desercion_2023)
# score_variation_by_speciality_chart(data_path=data_2023, puntaje='Examen')
# score_variation_by_speciality_chart(data_path=data_2023, puntaje='Puntaje final')
# score_variation_by_speciality_chart(data_path=data_2023, puntaje='Promedio')
# applicants_pie_chart(desertion_path=desercion_2023)
# vacancies_pie_chart(desertion_path=desercion_2023)

###### Para TODOS los años

make_reincidence_bar_plot(reincidence_path=reincidencia_2023)
# score_chart(data_paths=[data_2023, data_2022], years=[2023, 2022], puntaje='Examen', interval=1)
# score_chart(data_paths=[data_2023, data_2022], years=[2023, 2022], puntaje='Puntaje final', interval=1)
# score_chart(data_paths=[data_2023, data_2022], years=[2023, 2022], puntaje='Promedio', interval=1)
