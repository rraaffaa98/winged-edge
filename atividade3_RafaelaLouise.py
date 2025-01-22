Rafaela Louise dos Santos   ra:1991345
# Função para criar um novo vértice
def criar_vertice(vertices, x, y, z):
    vertice_id = len(vertices)
    vertice = {"id": vertice_id, "x": x, "y": y, "z": z, "edges": []}
    vertices.append(vertice)
    return vertice

# Função para criar uma nova aresta
def criar_aresta(arestas, vertice1, vertice2, face1=None, face2=None):
    aresta_id = len(arestas)
    aresta = {"id": aresta_id, "vertex1": vertice1, "vertex2": vertice2, "face1": face1, "face2": face2}
    arestas.append(aresta)
    vertice1["edges"].append(aresta)
    vertice2["edges"].append(aresta)
    return aresta

# Função para criar uma nova face
def criar_face(faces, vertices, arestas):
    face_id = len(faces)
    face = {"id": face_id, "vertices": vertices, "edges": []}
    faces.append(face)
    for i in range(len(vertices)):
        vertice1 = vertices[i]
        vertice2 = vertices[(i + 1) % len(vertices)]
        aresta = encontrar_aresta(vertice1, vertice2)
        if aresta:
            aresta["face2"] = face
        else:
            aresta = criar_aresta(arestas, vertice1, vertice2, face)
        face["edges"].append(aresta)

# Função para encontrar uma aresta entre dois vértices
def encontrar_aresta(vertice1, vertice2):
    for aresta in vertice1["edges"]:
        if aresta["vertex1"] == vertice1 and aresta["vertex2"] == vertice2:
            return aresta
    return None

# Função para encontrar as faces que compartilham uma aresta
def encontrar_faces_por_aresta(arestas, aresta_id):
    if 0 <= aresta_id < len(arestas):
        aresta = arestas[aresta_id]
        return [aresta["face1"]["id"] if aresta["face1"] else None, 
                aresta["face2"]["id"] if aresta["face2"] else None]
    return []

# Função para encontrar as arestas que compartilham um vértice
def encontrar_arestas_por_vertice(vertices, vertice_id):
    if 0 <= vertice_id < len(vertices):
        vertice = vertices[vertice_id]
        return vertice["edges"]
    return []

# Função para encontrar os vértices que compartilham uma face
def encontrar_vertices_por_face(faces, face_id):
    if 0 <= face_id < len(faces):
        face = faces[face_id]
        return face["vertices"]
    return []

# Função para ler o arquivo .obj e construir a estrutura winged-edge usando dicionários
def construir_estrutura_winged_edge(file_name):
    vertices = []
    arestas = []
    faces = []
    vertices_atuais = []

    with open(file_name, 'r') as obj_file:
        for line in obj_file:
            parts = line.split()
            if not parts:
                continue

            if parts[0] == 'v':
                x, y, z = map(float, parts[1:4])
                vertice = criar_vertice(vertices, x, y, z)
                vertices_atuais.append(vertice)
            elif parts[0] == 'f':
                vertex_indices = [int(v.split('//')[0]) - 1 for v in parts[1:]]
                face_vertices = [vertices_atuais[i] for i in vertex_indices]
                criar_face(faces, face_vertices, arestas)

    return vertices, arestas, faces

# Função principal para exibir o menu e interagir com o usuário
def main():
    obj_file = "cube.obj"
    vertices, arestas, faces = construir_estrutura_winged_edge(obj_file)

    while True:
        print("\nMenu:")
        print("1. Consultar as faces que compartilham uma aresta")
        print("2. Consultar as arestas que compartilham um vértice")
        print("3. Consultar os vértices que compartilham uma face")
        print("4. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            aresta_id = int(input("Informe o ID da aresta: "))
            shared_faces = encontrar_faces_por_aresta(arestas, aresta_id)
            print(f"Faces compartilhadas pela aresta {aresta_id}: {shared_faces}")
            input("Pressione Enter para voltar ao menu...")

        elif choice == "2":
            vertice_id = int(input("Informe o ID do vértice: "))
            shared_edges = encontrar_arestas_por_vertice(vertices, vertice_id)
            print(f"Arestas compartilhadas pelo vértice {vertice_id}: {[aresta['id'] for aresta in shared_edges]}")
            input("Pressione Enter para voltar ao menu...")

        elif choice == "3":
            face_id = int(input("Informe o ID da face: "))
            shared_vertices = encontrar_vertices_por_face(faces, face_id)
            print(f"Vértices compartilhados pela face {face_id}: {[vertice['id'] for vertice in shared_vertices]}")
            input("Pressione Enter para voltar ao menu...")

        elif choice == "4":
            break

if __name__ == "__main__":
    main()

