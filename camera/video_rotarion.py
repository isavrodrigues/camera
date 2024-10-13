import cv2
import numpy as np


def generate_coordinates_grid(height, width):
    """
    gera uma grade de coordenadas (y, x) que representam os indices de uma imagem
    com dimensões (height, width).
    """
    y_indices, x_indices = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    coords = np.stack([y_indices.ravel(), x_indices.ravel(), np.ones_like(y_indices).ravel()], axis=0)
    return coords

#funcao para aplicar rotacao e escala na imagem
def transform_image(image, angle, scale):
    img_height, img_width = image.shape[:2]
    transformed_image = np.zeros_like(image)

    #criar a grade de coordenadas (indices) da imagem
    coords = generate_coordinates_grid(img_height, img_width)

    #matriz de transformacao: translacao para o centro da imagem
    translate_to_center = np.array([[1, 0, -img_width // 2],
                                    [0, 1, -img_height // 2],
                                    [0, 0, 1]])

    #matriz de rotacao baseada no angulo
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                [np.sin(angle), np.cos(angle), 0],
                                [0, 0, 1]])

    #matriz de escala
    scale_matrix = np.array([[scale, 0, 0],
                             [0, scale, 0],
                             [0, 0, 1]])

    #matriz para desfazer a translacao apos a transformacao
    translate_back = np.array([[1, 0, img_width // 2],
                               [0, 1, img_height // 2],
                               [0, 0, 1]])

    #matriz de transformacao composta (combinacao de todas as transformacoes)
    transformation_matrix = translate_back @ scale_matrix @ rotation_matrix @ translate_to_center

    #aplica transformacao nas coordenadas
    transformed_coords = transformation_matrix @ coords
    transformed_coords = transformed_coords[:2, :]  # Remover a terceira linha (z = 1)

    #convertes para valores inteiros e garantir que fiquem dentro da imagem
    y_coords = np.clip(np.round(transformed_coords[0, :]).astype(int), 0, img_height - 1)
    x_coords = np.clip(np.round(transformed_coords[1, :]).astype(int), 0, img_width - 1)

    #aplica transformacao na imagem
    transformed_image[y_coords, x_coords] = image[coords[0, :], coords[1, :]]

    return transformed_image

#funcao principal para capturar o video e aplicar as transformacoes
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return

    #parametros iniciais
    angle = 0 
    rotation_speed = 0.1 
    scale_factor = 1.0  

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame!")
            break

        frame = cv2.resize(frame, (320, 240))
        image = frame.astype(np.float32) / 255.0
        transformed_image = transform_image(image, angle, scale_factor)
        cv2.imshow('Transformação em Tempo Real', transformed_image)


        key = cv2.waitKey(10) & 0xFF
        if key == ord('w'):
            rotation_speed += 0.01 
        elif key == ord('s'):
            rotation_speed -= 0.01 
        elif key == ord('e'):
            scale_factor += 0.05 
        elif key == ord('d'):
            scale_factor -= 0.05  
        elif key == ord('r'):
            angle = 0  
            rotation_speed = 0.1  
            scale_factor = 1.0  
        elif key == ord('q'):
            break  

        angle += rotation_speed

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()