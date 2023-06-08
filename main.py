import matplotlib
matplotlib.use('TkAgg')  # Cambiar el backend a TkAgg
import matplotlib.pyplot as plt
import pandas as pd
import fx_utils as fx_utils
import seaborn as sns


def get_promedio_especialidad(especialidad, resto):
    df = pd.read_csv('data/data.csv')
    filtro = df['especialidad'] == especialidad
    df = df[filtro]
    df = df.sort_values(by="promedio", ascending=False)
    if resto == 1:
        return df.iloc[-1]['promedio']
    return df.iloc[-resto - 1]['promedio']


def vacancies_applicants_chart():
    df = pd.read_csv('data/desercion.csv')
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Postulantes", ascending=False)
    df = df.drop('Total')

    ## Para seleccionar parte 1, parte 2 y parte 3
    # df = df[0:15]
    # df = df[15: 30]
    df = df[30:]
    max_applicants = df['Postulantes'].max()

    for especialidad in df.index:
        cupos = df.loc[especialidad]['Cupos']
        resto = df.loc[especialidad]['Resto']
        postulantes = df.loc[especialidad]['Postulantes']
        especialidad_label = fx_utils.replace_speciality_names(especialidad)
        if resto > 0:
            plt.bar(especialidad_label, [cupos], color=celeste)
            plt.bar(especialidad_label, [resto], bottom=cupos, color=rojo)
            promedio = get_promedio_especialidad(especialidad=especialidad, resto=resto)
            plt.text(especialidad_label, cupos + (max_applicants * 0.04), str(promedio), ha='center', va='top')
            # plt.text(especialidad_label, postulantes, str(promedio), ha='center', va='top')
        elif resto < 0:
            plt.bar(especialidad_label, [postulantes], color=celeste)
            plt.bar(especialidad_label, [resto * (-1)], bottom=postulantes, color=verde)
        else:
            plt.bar(especialidad_label, [postulantes], color=celeste)

    referencias = [plt.Rectangle((0, 0), 1, 1, color=celeste),
                   plt.Rectangle((0, 0), 1, 1, color=rojo),
                   plt.Rectangle((0, 0), 1, 1, color=verde)]
    plt.legend(referencias, ['Cupos tomados', 'Postulantes sin cupo', 'Cupos sobrantes'])
    plt.tick_params(axis='x', labelrotation=45)
    plt.title('Habilitados y Cupos (promedios limites en postulantes sin cupo)')
    plt.xlabel('Especialidad')
    plt.ylabel('Cupos, Postulantes')
    plt.show()


def desertion_chart():
    desercion_df = pd.read_csv('data/desercion.csv')
    filter = desercion_df['Resto'] > 0
    desercion_df = desercion_df[filter].sort_values(by='Resto', ascending=False)
    desercion_df = desercion_df.drop(45)
    desercion_df['Especialidad'] = desercion_df['Especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    desercion_df = desercion_df[0:20]

    plt.bar(desercion_df['Especialidad'], desercion_df['Resto'], color=rojo)
    for i, valor in enumerate(desercion_df['Resto']):
        plt.annotate(str(valor), xy=(i, valor), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=10)
    plt.tick_params(axis='x', labelrotation=45, labelsize=8)
    plt.suptitle('Postulantes sin cupo segun especialidad')
    plt.title('(2424 postulantes totales sin cupo)', fontsize=10)
    plt.xlabel('Especialidad')
    plt.ylabel('Postulantes sin cupos')
    plt.show()


def free_vacancies_chart():
    desercion_df = pd.read_csv('data/desercion.csv')
    desercion_df['Especialidad'] = desercion_df['Especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    filter = desercion_df['Resto'] < 0
    desercion_df['Resto'] = desercion_df['Resto'].apply(lambda x: x * -1)
    desercion_df = desercion_df[filter].sort_values(by='Resto', ascending=False)
    total = desercion_df['Resto'].sum()
    plt.bar(desercion_df['Especialidad'], desercion_df['Resto'], color=verde)
    for i, valor in enumerate(desercion_df['Resto']):
        plt.annotate(str(valor), xy=(i, valor), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=10)
    plt.tick_params(axis='x', labelrotation=45, labelsize=8)
    plt.suptitle('Cupos libres segun especialidad', fontsize=13)
    plt.title(f'({total} cupos libres en total)', fontsize=9)
    plt.xlabel('Especialidad')
    plt.ylabel('Cupos libres')
    plt.show()


def score_variation_by_speciality_chart():
    score_df = pd.read_csv('data/data.csv')
    score_df['especialidad'] = score_df['especialidad'].apply(lambda x: fx_utils.replace_speciality_names(x))
    medians = score_df.groupby('especialidad')['promedio'].median()
    score_df['median'] = score_df['especialidad'].map(medians)
    score_df = score_df.sort_values('median')

    unique_specialities = list(score_df['especialidad'].unique())
    p1 = unique_specialities[:int(len(unique_specialities) / 2)]
    p2 = unique_specialities[int(len(unique_specialities) / 2):]

    for i, parte in enumerate([p1, p2]):
        grupo = score_df[score_df['especialidad'].isin(parte)]

        sns.boxplot(x='especialidad', y='promedio', data=grupo)

        plt.xlabel('Especialidad')
        plt.ylabel('Promedio')
        plt.suptitle('Distribución del promedio por especialidad', fontsize=15)
        plt.tick_params(axis='x', labelrotation=45, labelsize=8)

        # plt.savefig(f'./images/score/score_box_chart_p{i + 1}.png', dpi=300)
        plt.show()


def score_chart():
    score_df = pd.read_csv('data/data.csv')
    score_df = score_df.dropna(how='all')
    score_df = score_df.sort_values('promedio')

    ## Media total
    media = score_df['promedio'].mean()

    conteo = score_df['promedio'].dropna()

    ## Redondear por 0.25
    # conteo = conteo.apply(lambda x: round(x * 4) / 4)
    ## Redondear por 0.2
    conteo = conteo.apply(lambda x: round(x * 5) / 5)
    ## Redondear por 0.1
    # conteo = conteo.apply(lambda x: round(x * 10) / 10)

    conteo = conteo.value_counts().sort_index()

    plt.plot(conteo.index, conteo.values, color=celeste)
    plt.scatter(conteo.index, conteo.values, color=celeste)
    plt.xlabel('Promedios')
    plt.ylabel('Cantidad')
    plt.suptitle('Distribucion de promedios general', fontsize=13)
    plt.title(f'(Media de {round(media, 2)})', fontsize=9)
    plt.show()


def applicants_pie_chart():
    df = pd.read_csv('data/desercion.csv')
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Postulantes", ascending=False)
    df = df.drop('Total')

    threshold = 1.5
    total = sum(df['Postulantes'])
    df['Porcentaje'] = df['Postulantes'].apply(lambda x: round((x / total) * 100, 1))
    others_df = df[df['Porcentaje'] < threshold]
    upper_df = df[df['Porcentaje'] > threshold]
    others_for_pie_df = others_df.sum().T
    others_for_pie_df.name = f'Otros (< {threshold}%)'
    upper_df = upper_df._append(others_for_pie_df)
    plt.pie(upper_df['Porcentaje'], labels=[fx_utils.replace_speciality_names(label) for label in upper_df.index], autopct='%1.1f%%', startangle=90)
    plt.title('% Postulantes a especialidad', fontsize=13)
    plt.savefig('./images/applicants/applicants_pie.png')
    plt.show()


def vacancies_pie_chart():
    df = pd.read_csv('data/desercion.csv')
    df = df.set_index('Especialidad')
    df = df.sort_values(by="Cupos", ascending=False)
    df = df.drop('Total')

    threshold = 1.2
    total = sum(df['Cupos'])
    df['Porcentaje'] = df['Cupos'].apply(lambda x: round((x / total) * 100, 1))
    others_df = df[df['Porcentaje'] < threshold]
    upper_df = df[df['Porcentaje'] > threshold]
    others_for_pie_df = others_df.sum().T
    others_for_pie_df.name = f'Otros (< {threshold}%)'
    upper_df = upper_df._append(others_for_pie_df)

    plt.pie(upper_df['Porcentaje'], labels=[fx_utils.replace_speciality_names(label) for label in upper_df.index], autopct='%1.1f%%', startangle=90)
    plt.title('% Cupos oficiales por especialidad', fontsize=13)
    plt.savefig('./images/vacancies/vacancies_pie.png')
    plt.show()


celeste = "#087E8B"
verde = "#548C2F"
rojo = "#EA7317"

### Ejecutar los diferentes plots

vacancies_applicants_chart()
desertion_chart()
free_vacancies_chart()
score_variation_by_speciality_chart()
score_chart()
applicants_pie_chart()
vacancies_pie_chart()
