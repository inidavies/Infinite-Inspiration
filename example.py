from color import background_color


# How the import works- if you just import color then you can access background color by 
# doing color.background_color

# Will consistently timeout with google images (returns -1)
print(f'Google Images: {background_color("https://images.app.goo.gl/evYzWkv18hiun6bT6"}'))

# Will work well with bing and unsplash and also tinyurl versions of these
print(f'Bing Images: {background_color("https://th.bing.com/th/id/OIP.LIyeXFdvM83UkH_jNud3zwHaE5?pid=ImgDet&rs=1")}') 
print(f'Unsplash: {background_color("https://source.unsplash.com/gySMaocSdqs/w=600")}')