# pylint: disable=C0301, C0114, C0116, W0621

import os
import re
import networkx as nx
import matplotlib.pyplot as plt


def read_files(directory):
    files_content = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                files_content[filename] = file.read()
    return files_content


def extract_dependencies(files_content):
    dependency_pattern = re.compile(r"(import|new) UserScript/(\w+)")
    dependencies = {}
    for filename, content in files_content.items():
        dependencies[filename] = set()
        for match in dependency_pattern.finditer(content):
            dependency = f"{match.group(2)}.txt"
            if (
                dependency != filename and dependency != "s.txt"
            ):  # Exclude self and s.txt dependencies
                dependencies[filename].add(dependency)
    return dependencies


def simplify_dependencies(dependencies):
    simplified = {}
    for file, deps in dependencies.items():
        if len(deps) == 1:
            dep = next(iter(deps))
            if dependencies.get(dep) == {file}:
                # Merge file and dep into a single node
                new_node = f"{file.replace('.txt', '')}-{dep.replace('.txt', '')}"
                simplified[new_node] = {new_node}
                continue
        simplified[file] = deps
    return simplified


def build_dependency_graph(dependencies):
    graph = nx.DiGraph()
    level_files = {f"{i:02}_".format(i) for i in range(8)}  # Set of level file prefixes

    for file, deps in dependencies.items():
        node = (
            "levels"
            if any(file.startswith(prefix) for prefix in level_files)
            else file.replace(".txt", "")
        )
        for dep in deps:
            dep_node = (
                "levels"
                if any(dep.startswith(prefix) for prefix in level_files)
                else dep.replace(".txt", "")
            )
            if dep_node != "s":  # Exclude s.txt dependencies
                graph.add_edge(node, dep_node)

    # Remove self-loops that might have been created by the level grouping
    graph.remove_edges_from(nx.selfloop_edges(graph))

    return graph


def visualize_dependency_graph(graph, output_file="dependency_graph.png"):
    plt.figure(figsize=(10, 10))
    pos = nx.shell_layout(graph)  # Use shell layout to avoid overlapping nodes
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=5300,
        node_color="skyblue",
        font_size=13,
        font_weight="bold",
        arrowsize=23,
        edge_color="gray",
    )
    plt.title("Stonescript Dependency Graph", fontsize=15)
    plt.savefig(output_file)
    plt.show()


if __name__ == "__main__":
    DIRECTORY = r"D:\Programs\SteamLibrary\steamapps\common\Stone Story RPG\StoneScript"  # path containing Stonescript files
    files_content = read_files(DIRECTORY)
    dependencies = extract_dependencies(files_content)
    simplified_dependencies = simplify_dependencies(dependencies)
    dependency_graph = build_dependency_graph(simplified_dependencies)
    visualize_dependency_graph(dependency_graph)
