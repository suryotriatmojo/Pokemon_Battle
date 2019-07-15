from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
import requests, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

app = Flask(__name__)

# home route
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        pokemon_1 = request.form['pokemon1']
        pokemon_1 = pokemon_1.lower()
        pokemon_2 = request.form['pokemon2']
        pokemon_2 = pokemon_2.lower()

        df_1 = df_pokemon[df_pokemon['Name'] == pokemon_1.title()]
        df_2 = df_pokemon[df_pokemon['Name'] == pokemon_2.title()]
        df_gabung = pd.concat([df_1, df_2], axis = 0)

        id_1 = df_gabung['#'].values[0]
        id_2 = df_gabung['#'].values[1]

        hp_1 = df_gabung['HP'].loc[id_1 - 1]
        attack_1 = df_gabung['Attack'].loc[id_1 - 1]
        defense_1 = df_gabung['Defense'].loc[id_1 - 1]
        sp_atk_1 = df_gabung['Sp. Atk'].loc[id_1 - 1]
        sp_def_1 = df_gabung['Sp. Def'].loc[id_1 - 1]
        speed_1 = df_gabung['Speed'].loc[id_1 - 1]
        
        hp_2 = df_gabung['HP'].loc[id_2 - 1]
        attack_2 = df_gabung['Attack'].loc[id_2 - 1]
        defense_2 = df_gabung['Defense'].loc[id_2 - 1]
        sp_atk_2 = df_gabung['Sp. Atk'].loc[id_2 - 1]
        sp_def_2 = df_gabung['Sp. Def'].loc[id_2 - 1]
        speed_2 = df_gabung['Speed'].loc[id_2 - 1]

        pred = log_reg.predict([[
            hp_1, attack_1, defense_1, sp_atk_1, sp_def_1, speed_1,
            hp_2, attack_2, defense_2, sp_atk_2, sp_def_2, speed_2
        ]])[0]

        if pred == 0:
            winner = pokemon_1.title()
        else:
            winner = pokemon_2.title()

        prob = log_reg.predict_proba([[
            hp_1, attack_1, defense_1, sp_atk_1, sp_def_1, speed_1,
            hp_2, attack_2, defense_2, sp_atk_2, sp_def_2, speed_2
        ]]).max()
        prob = round(prob * 100, 2)
        
        url_1='https://pokeapi.co/api/v2/pokemon/'+pokemon_1
        url_1 = requests.get(url_1)
        url_2='https://pokeapi.co/api/v2/pokemon/'+pokemon_2
        url_2 = requests.get(url_2)

        if str(url_1) == '<Response [404]>':
            abort(404)
        if str(url_2) == '<Response [404]>':
            abort(404)

        pic_1 = url_1.json()['sprites']['front_default']
        pic_2 = url_2.json()['sprites']['front_default']

        # plotting        
        plt.figure('Pokemon Stats', figsize = (15,5))

        plt.subplot(161)
        plt.bar(df_gabung['Name'], df_gabung['HP'], color = ('blue', 'green'))
        plt.title('HP')
        # for i in range(len(df_gabung)):
        #     plt.text(df_gabung['Name'][i], df_gabung['HP'][i] + 0.2, df_gabung['HP'][i])

        plt.subplot(162)
        plt.bar(df_gabung['Name'], df_gabung['Attack'], color = ('blue', 'green'))
        plt.title('Attack')
        # for i in range(len(df_gabung)):
        #     plt.text(df_gabung['Name'][i], df_gabung['Attack'][i] + 0.2, df_gabung['Attack'][i])

        plt.subplot(163)
        plt.bar(df_gabung['Name'], df_gabung['Defense'], color = ('blue', 'green'))
        plt.title('Defense')
        # for i in range(len(df_gabung)):
        #     plt.text(df_gabung['Name'][i], df_gabung['Defense'][i] + 0.2, df_gabung['Defense'][i])

        plt.subplot(164)
        plt.bar(df_gabung['Name'], df_gabung['Sp. Atk'], color = ('blue', 'green'))
        plt.title('Sp. Atk')
        # for i in range(len(df_gabung)):
        #     plt.text(df_gabung['Name'][i], df_gabung['Sp. Atk'][i] + 0.2, df_gabung['Sp. Atk'][i])

        plt.subplot(165)
        plt.bar(df_gabung['Name'], df_gabung['Sp. Def'], color = ('blue', 'green'))
        plt.title('Sp. Def')
        # for i in range(len(df_gabung)):
        #     plt.text(df_gabung['Name'][i], df_gabung['Sp. Def'][i] + 0.2, df_gabung['Sp. Def'][i])

        plt.subplot(166)
        plt.bar(df_gabung['Name'], df_gabung['Speed'], color = ('blue', 'green'))
        plt.title('Speed')
        # for i in range(len(df_gabung)):
        #     plt.text(df_gabung['Name'][i], df_gabung['Speed'][i] + 0.2, df_gabung['Speed'][i])

        plt.tight_layout()

        path = os.listdir('./storage')
        name_file = 'Pokemon Battle Stats.jpg'
        plt.savefig('storage/%s' % name_file)

        return render_template('hasil.html', nama_1 = pokemon_1.title(), nama_2 = pokemon_2.title(), gambar_1 = pic_1, gambar_2 = pic_2, winner = winner, proba = prob, plot = name_file)
    else:        
        return render_template('home.html')

# path route
@app.route('/plot/<path:x>')
def show_plot(x):
    return send_from_directory('storage', x)

# show error not found route
@app.errorhandler(404)
def error(error):
    return render_template('error.html')

if __name__ == '__main__':
    df_pokemon = pd.read_csv('Dataset_3/pokemon.csv')
    log_reg = joblib.load('model_pokemon_battle')
    app.run(debug = True)