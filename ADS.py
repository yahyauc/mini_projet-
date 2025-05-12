import numpy as np


ADS = np.array([
    [22.5, 122332, 45],
    [19.1, 132494, 50],
    [21.4, 128277, 47],
    [20.0, 232443, 48],
    [19.7, 232432, 49],
])

#display the dimension
print("Dimension:")
print(ADS.ndim)

# !!!!!!!
print("")
print(ADS.shape)

# display type of data
print(ADS.dtype)

# display the element
print(ADS.size)

# extract the colmun of temp
print(ADS[:,[2]])

#some operations
print(np.mean(ADS, 0 ))
print(np.median(ADS, 0))
print(np.var(ADS, 0))
print(np.std(ADS, 0))



'''
#min
print(np.min(ADS[:, 0]))
print(np.min(ADS[:, 1]))
print(np.min(ADS[:, 2]))
#max
print(np.max(ADS[:, 0]))
print(np.max(ADS[:, 1]))
print(np.max(ADS[:, 2]))
'''


#error
#!!!!!!
print(np.min(ADS, axis = 0))


'''
print(ADS.max(axis = 0))
'''

#temp
temp = ADS[:, 0]

print(ADS[temp > 21])

Fahrenheit = temp*9/5 + 32
ADS = np.column_stack((ADS, Fahrenheit))


# delete
print(np.delete(ADS,1, axis=1))


print(ADS*1.1)

print(np.sum(ADS, 1))

print(np.sum(ADS, 0))

print(ADS.T)

print(np.where(ADS > 300, 300, ADS))
