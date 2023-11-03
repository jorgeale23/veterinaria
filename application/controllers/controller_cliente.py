from application import app
from flask import Flask, jsonify
from flask import render_template, request, redirect, url_for, flash, session
from application.models.model_cliente import ClienteDAO, Cliente  # Importamos DAO y DTO
from application.config.routes import urls

# Creamos un Service Locator para obtener instancias de ClienteDAO
class ServiceLocator():
    def __init__(self):
        self.cliente_dao = ClienteDAO()

locator = ServiceLocator()

@app.route(urls['index'], methods = ['GET'])
def index():
    session['user'] = True
    if session['user']:
        data = { "cliente" : locator.cliente_dao.get_all_clientes() }  # Usamos el DAO para obtener los clientes
        lista_clientes = [] # Creamos una lista de clientes
        for cliente_data in data:
            cliente = Cliente(cliente_data["nombre"], cliente_data["telefono"], cliente_data["email"])
            lista_clientes.append(cliente)
        return render_template('index.html', data = lista_clientes) #Enviamos lista de clientes
    else:
        return redirect(url_for('login'))

@app.route(urls['add.user'] , methods = ['POST'])
def add():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']
            cliente = Cliente(cliente_data[nombre], cliente_data[telefono], cliente_data[email])
            locator.cliente_dao.add_cliente(cliente)  # Usamos el DAO para agregar el cliente
            flash('Cliente guardado!')
            return redirect(url_for('index'))
        except:
            flash('¡Ha ocurrido un error!')
            return redirect(url_for('index'))

@app.route(urls['delete.user'] , methods = ['GET'])
def delete(id):
    res = locator.cliente_dao.delete_cliente(id)  # Usamos el DAO para eliminar el cliente
    if res == 1:
        flash('Cliente Eliminado...')
    else:
        flash('¡Ha ocurrido un error...')
    return redirect(url_for('index'))

@app.route(urls['update.user'] , methods = ['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cliente = Cliente(nombre, None, telefono, email)  # Creamos un DTO con los datos actualizados
        res = locator.cliente_dao.update_cliente(cliente_dto)  # Usamos el DAO para actualizar el cliente
        if res == 1:
            flash('Cliente Actualizado...')
            return redirect(url_for('index'))
        else:
            flash('Error al actualizar...')
            return redirect(url_for('index'))
    elif request.method == 'GET':
        contacto = locator.cliente_dao.get_by_id(id)  # Usamos el DAO para obtener un cliente por su ID
        return render_template('edit.html', cliente = cliente[0])

