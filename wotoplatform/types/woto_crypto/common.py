#  WotoPlatform-Py - A Python library for interacting with WotoPlatform API.
#  Copyright (C) 2021-2022  ALiwoto - <woto@kaizoku.cyou> <https://github.com/ALiwoto>
#
#  This file is part of WotoPlatform-Py.
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import typing
from enum import Enum
from pydantic import BaseModel


__CR_LAYER_FACTOR__ = 0x1b
__BA_ALGORITHM_FACTOR__ = 0x2

class WotoAlgorithm(Enum):
    M250 = 0x40
    M251 = 0x30
    M252 = 0x28
    M253 = 0x20

class BlockAlgorithmId(Enum):
    X917 = __BA_ALGORITHM_FACTOR__ << 0x0
    X847 = __BA_ALGORITHM_FACTOR__ << 0x1
    X795 = __BA_ALGORITHM_FACTOR__ << 0x2
    X649 = __BA_ALGORITHM_FACTOR__ << 0x3


class CryptoLayerKind(Enum):
    O27 = __CR_LAYER_FACTOR__ << 0x0
    O54 = __CR_LAYER_FACTOR__ << 0x1
    O108 = __CR_LAYER_FACTOR__ << 0x2
    O216 = __CR_LAYER_FACTOR__ << 0x3



class WotoLayerLength(int):
    pass

class _PrivateBlock(int):
    pass


__layer_kinds_map__ = {
    CryptoLayerKind.O27: True,
    CryptoLayerKind.O54: True,
    CryptoLayerKind.O108: True,
    CryptoLayerKind.O216: True,
}

__layer_length_validator = {
    CryptoLayerKind.O27: lambda x: x == 0x27,
    CryptoLayerKind.O54: lambda x: x == 0x54,
    CryptoLayerKind.O108: lambda x: x == 0x108,
    CryptoLayerKind.O216: lambda x: x == 0x216,
}

class WotoValidator():
    def is_valid(self) -> bool:
        pass


class WotoSerializer(BaseModel):
    def serialize_object(self) -> bytes:
        pass

    def str_serialize(self) -> str:
        pass


class BytesObject():
    def to_bytes(self) -> bytes:
        pass

    def get_length(self) -> int:
        pass

def __encrypt_data__(key: bytes, data: bytes) -> bytes:
    key_blocks = __to_block_collection(key)
    data_blocks = __to_block_collection(data)
    return __encrypt_by_blocks(key_blocks, data_blocks, None)

def __decrypt_data__(key: bytes, data: bytes) -> bytes:
    key_blocks = __to_block_collection(key)
    data_blocks = __to_block_collection(data)
    return __decrypt_by_blocks(key_blocks, data_blocks, None)

def __encrypt_by_blocks(key: '_BlockCollection', data: '_BlockCollection', algorithm: '_BlockAlgorithm') -> bytes:
    pass

def __decrypt_by_blocks(key: '_BlockCollection', data: '_BlockCollection', algorithm: '_BlockAlgorithm') -> bytes:
    pass

def __to_block_collection(data: bytes) -> '_BlockCollection':
    return _PrivateCollection(data)

class _PrivateCollection:
    blocks: typing.List[_PrivateBlock]

    def __init__(self, data: bytes):
        my_data = data.decode('utf-8')
        self.blocks = []
        for current in my_data:
            self.blocks.append(_PrivateBlock(ord(current)))

class LayerLengthContainer(BaseModel, WotoValidator):
    length: WotoLayerLength = 0
    layer_kind: CryptoLayerKind = CryptoLayerKind.O27

    def is_valid(self) -> bool:
        return self.length > 0

    

class CryptoLayer(BaseModel, WotoValidator):
    kind: CryptoLayerKind
    hash: str
    lenContainer: typing.Optional[LayerLengthContainer] = None

    def get_layer_length(self) -> LayerLengthContainer:
        if self.lenContainer is not None and self.lenContainer.is_valid():
            return self.lenContainer
        self.lenContainer = self.get_new_layer_container()
        return self.lenContainer
    
    def to_map(self):
        return {
            'kind': self.kind.value,
            'hash': self.hash
        }
    
    def get_new_layer_container(self) -> LayerLengthContainer:
        return LayerLengthContainer(length=self.get_length(), layer_kind=self.kind)
    
    def get_length(self) -> WotoLayerLength:
        return WotoLayerLength(len(self.hash))
    
    def is_valid(self) -> bool:
        return self.get_layer_length().is_valid()
    
    def to_bytes(self) -> bytes:
        if not self.is_valid():
            raise Exception("Invalid CryptoLayer")
        return bytes(self.hash, encoding='utf-8')
    
    def is_equal(self, layer: 'CryptoLayer') -> bool:
        return self.hash == layer.hash and self.kind == layer.kind

class KeyLayerCollection(typing.List[CryptoLayer]):
    def get_layer_by_index(self, index: int) -> CryptoLayer:
        if index >= len(self):
            return None
        return self[index]
    
    def is_valid(self) -> bool:
        return len(self) != 0 and self.validate_keys()
    
    def validate_keys(self) -> bool:
        for current in self:
            if not current.is_valid():
                return False
        return True

    def to_list(self):
        return [current.to_map() for current in self]
    
    def contains(self, layer: CryptoLayer) -> bool:
        for current in self:
            if current.is_equal(layer):
                return True
        return False
    
    def contains_kind(self, kind: CryptoLayerKind) -> bool:
        for current in self:
            if current.kind == kind:
                return True
        return False
    
    def get_key_length(self) -> int:
        total = 0
        for current in self:
            total += int(current.get_length())
        return total
    

    def get_layer_length_by_kind(self, kind: CryptoLayerKind) -> LayerLengthContainer:
        for current in self:
            if current.kind == kind:
                return current.get_layer_length()
        return None

class _BlockAlgorithmX917(BaseModel):
    identifier: int


class _BlockAlgorithmX847(BaseModel):
    identifier: int


class _BlockAlgorithmX795(BaseModel):
    identifier: int


class _BlockAlgorithmX649(BaseModel):
    identifier: int


class AlgorithmSupporter(BaseModel):
    """
    SetAlgorithm(algorithm WotoAlgorithm) bool
	HasEqualAlgorithm(algorithm WotoAlgorithm) bool
	GetAlgorithm() WotoAlgorithm
	GetHashCount() int
    """
    def set_algorithm(self, algorithm: WotoAlgorithm) -> bool:
        pass

    def has_equal_algorithm(self, algorithm: WotoAlgorithm) -> bool:
        pass

    def get_algorithm(self) -> WotoAlgorithm:
        pass

    def get_gash_count(self) -> int:
        pass


class LayerBlock(BaseModel):
    """
    ContainsLayerKind(kind CryptoLayerKind) bool
	ContainsLayer(layer *CryptoLayer) bool
	AppendLayer(layer *CryptoLayer) bool
	RemoveLayer(layer *CryptoLayer) bool
	RemoveLayers(layers ...*CryptoLayer)
	GetLayerLengthByKind(kind CryptoLayerKind) *LayerLengthContainer
	GetLayerLengthByIndex(index int) *LayerLengthContainer
	GetKeyLayersCount() int
    """
    def contains_layer_kind(self, kind: CryptoLayerKind) -> bool:
        pass

    def contains_layer(self, layer: CryptoLayer) -> bool:
        pass

    def append_layer(self, layer: CryptoLayer) -> bool:
        pass

    def remove_layer(self, layer: CryptoLayer) -> bool:
        pass

    def remove_layers(self, layers: typing.List[CryptoLayer]):
        pass

    def get_layer_length_by_kind(self, kind: CryptoLayerKind) -> LayerLengthContainer:
        pass

    def get_layer_length_by_index(self, index: int) -> LayerLengthContainer:
        pass

    def get_key_layers_count(self) -> int:
        pass


class SignatureContainer():
    def get_signature(self) -> str:
        pass

    def set_signature(self, signature: str) -> bool:
        pass

    def set_signature_by_bytes(self, signature: bytes) -> bool:
        if not signature:
            return False
        return self.set_signature(signature.decode('utf-8'))


class IntegerRepresent():
    def to_int(self) -> int:
        pass


class BitsBlocks():
    def get_bits_size() -> int:
        pass

class WotoKey(WotoValidator, LayerBlock, AlgorithmSupporter, WotoSerializer, SignatureContainer):
    """
	IsFuture() bool
	IsPast() bool
	IsPresent() bool
	IsEmpty() bool
	CanBecomeFuture() bool
	CanBecomePresent() bool
	CanBecomePast() bool
	Decrypt(data []byte) []byte
	Encrypt(data []byte) []byte
	HasEqualKind(key WotoKey) bool
	HasEqualSignature(key WotoKey) bool
	GetKeyLength() int
	GetSignatureRealLength() int
	IsRealLengthInvalid() bool

	// Deprecated: you can't convert any WotoKey to a FutureKey anymore.
	// Please use GenerateFutureKey helper function.
	ToFutureKey() WotoKey
	ToPresentKey() WotoKey
	ToPastKey() WotoKey
	Clone() WotoKey

	getLayers() KeyLayerCollection
	setLayers(layers KeyLayerCollection) bool
    """

    def is_future(self) -> bool:
        pass

    def is_past(self) -> bool:
        pass

    def is_present(self) -> bool:
        pass

    def is_empty(self) -> bool:
        pass

    def can_become_future(self) -> bool:
        pass

    def can_become_present(self) -> bool:
        pass

    def can_become_past(self) -> bool:
        pass

    def decrypt_data(self, data: bytes) -> bytes:
        pass

    def encrypt_data(self, data: bytes) -> bytes:
        pass

    def has_equal_kind(self, key: 'WotoKey') -> bool:
        pass

    def has_equal_signature(self, key: 'WotoKey') -> bool:
        pass

    def get_key_length(self) -> int:
        pass

    def get_signature_real_length(self) -> int:
        pass

    def is_real_length_invalid(self) -> bool:
        pass

    def to_future_key(self) -> 'WotoKey':
        pass

    def to_present_key(self) -> 'WotoKey':
        pass

    def to_past_key(self) -> 'WotoKey':
        pass

    def clone(self) -> 'WotoKey':
        pass

    def _get_layers(self) -> typing.List[CryptoLayer]:
        pass

    def _set_layers(self, layers: typing.List[CryptoLayer]) -> bool:
        pass

    


class KeyCollection(BaseModel, WotoValidator):
    def continue_life_cycle(self):
        pass

    def sync(self):
        pass


class KeysContainer():
    def set_as_keys(self, value: KeyCollection):
        pass


class _SingleBlock(WotoValidator, BitsBlocks):
    """
    IsEmpty() bool
	IsNonZero() bool
	ToInt64() int64
	ToUInt64() uint64
	ToInt32() int32
	ToUInt32() uint32
	Sum(singleBlock) singleBlock
	Min(singleBlock) singleBlock
	Mul(singleBlock) singleBlock
	Div(singleBlock) singleBlock
    """

    def is_empty(self) -> bool:
        pass

    def is_non_zero(self) -> bool:
        pass

    def to_int64(self) -> int:
        pass

    def to_uint64(self) -> int:
        pass

    def to_int32(self) -> int:
        pass

    def to_uint32(self) -> int:
        pass

    def sum(self, singleBlock: '_SingleBlock') -> '_SingleBlock':
        pass

    def min(self, singleBlock: '_SingleBlock') -> '_SingleBlock':
        pass

    def mul(self, singleBlock: '_SingleBlock') -> '_SingleBlock':
        pass

    def div(self, singleBlock: '_SingleBlock') -> '_SingleBlock':
        pass


# type blockAction func(first, second singleBlock) singleBlock

class _BlockAction(typing.Callable[[_SingleBlock, _SingleBlock], _SingleBlock]):
    pass

class _BlockCollection(BytesObject):
    """
    GetBlocks() []singleBlock
	GetRelativeIndex(int) int
	BlockSize() int
	AppendBlock(singleBlock)
	AppendCollection(blockCollection)
	GetBlockByIndex(int) singleBlock
	Clone() blockCollection
    """

    def get_blocks(self) -> typing.List[_SingleBlock]:
        pass

    def get_relative_index(self, index: int) -> int:
        pass

    def block_size(self) -> int:
        pass

    def append_block(self, singleBlock: _SingleBlock):
        pass

    def append_collection(self, blockCollection: '_BlockCollection'):
        pass

    def get_block_by_index(self, index: int) -> _SingleBlock:
        pass

    def clone(self) -> '_BlockCollection':
        pass

#2028391795 https://t.me/SpaceXSupports

class _BlockAlgorithm():
    """
    GetEncryptBlockAction(index int) blockAction
	GetDecryptBlockAction(index int) blockAction
    """

    def get_encrypt_block_action(self, index: int) -> _BlockAction:
        pass

    def get_decrypt_block_action(self, index: int) -> _BlockAction:
        pass



class _FutureKey(WotoKey):
    key_layers: KeyLayerCollection
    algorithm: WotoAlgorithm
    sig: str

    def to_future_key(self) -> 'WotoKey':
        return self
    
    def to_present_key(self) -> 'WotoKey':
        return _PresentKey(self.key_layers, self.algorithm, self.sig)
    
    def to_past_key(self) -> 'WotoKey':
        return None


class _PresentKey(WotoKey):
    key_layers: KeyLayerCollection
    algorithm: WotoAlgorithm
    sig: str
    def __init__(self, keyLayers: 'KeyLayerCollection', algorithm: 'WotoAlgorithm', sig: str):
        self.key_layers = keyLayers
        self.algorithm = algorithm
        self.sig = sig

    

    """

func (p *presentKey) GetLayers() KeyLayerCollection {
	return p.keyLayers
}

func (p *presentKey) GetLayerLengthByIndex(index int) *LayerLengthContainer {
	return p.keyLayers.GetLayerByIndex(index).GetLayerLength()
}

func (p *presentKey) SetLayers(layers KeyLayerCollection) bool {
	if !layers.IsValid() || !p.isValidWithAlgo(layers) {
		return false
	}

	p.keyLayers = layers

	return true
}

func (p *presentKey) isValidWithAlgo(layers KeyLayerCollection) bool {
	return true
}

func (p *presentKey) SetAlgorithm(algorithm WotoAlgorithm) bool {
	p.algorithm = algorithm
	return true
}

func (p *presentKey) GetSignature() string {
	return p.sig
}

func (p *presentKey) IsValid() bool {
	return p != nil && !p.IsEmpty() && p.sig != ""
}

func (p *presentKey) IsEmpty() bool {
	return len(p.keyLayers) == 0x0
}

func (p *presentKey) SetSignature(signature string) bool {
	if signature == "" {
		return false
	}

	p.sig = signature
	return true
}

func (p *presentKey) SetSignatureByBytes(data []byte) bool {
	if len(data) == 0 {
		return false
	}
	return p.SetSignature(string(data))
}

func (p *presentKey) SetSignatureByFunc(h func() hash.Hash) bool {
	if h == nil {
		return false
	}
	return p.SetSignatureByBytes(h().Sum(nil))
}

func (p *presentKey) Encrypt(data []byte) []byte {
	if !p.IsValid() {
		return data
	}

	switch p.algorithm {
	case WotoAlgorithmM250:
		return p.encryptM250(data)
	}
	return nil
}

func (p *presentKey) Serialize() ([]byte, error) {
	if !p.IsValid() {
		return nil, ErrInvalidKey
	}

	b, err := json.Marshal(p.toMap())
	if err != nil {
		return nil, err
	}

	return b, nil
}

func (p *presentKey) StrSerialize() string {
	b, err := p.Serialize()
	if err != nil || len(b) == 0 {
		return ""
	}

	return string(b)
}

func (p *presentKey) toMap() map[string]interface{} {
	return map[string]interface{}{
		"key_layers": p.keyLayers,
		"signature":  p.sig,
		"algorithm":  p.algorithm,
	}
}

func (p *presentKey) Decrypt(data []byte) []byte {
	if !p.IsValid() {
		return data
	}

	switch p.algorithm {
	case WotoAlgorithmM250:
		return p.decryptM250(data)
	}
	return nil
}

func (p *presentKey) encryptM250(data []byte) []byte {
	currentKey, err := p.keyLayers[0x0].ToBytes()
	if err != nil {
		return nil
	}
	var buff []byte

	for i, currentLayer := range p.keyLayers {
		if i == 0x0 {
			continue
		}

		buff, err = currentLayer.ToBytes()
		if err != nil {
			return nil
		}

		currentKey = EncryptData(currentKey, buff)
	}

	return EncryptData(currentKey, data)
}

func (p *presentKey) decryptM250(data []byte) []byte {
	currentKey, err := p.keyLayers[0x0].ToBytes()
	if err != nil {
		return nil
	}

	var buff []byte
	for i, currentLayer := range p.keyLayers {
		if i == 0x0 {
			continue
		}

		buff, err = currentLayer.ToBytes()
		if err != nil {
			return nil
		}

		currentKey = EncryptData(currentKey, buff)
	}

	return DecryptData(currentKey, data)
}

func (p *presentKey) AppendLayer(layer *CryptoLayer) bool {
	if !layer.IsValid() {
		return false
	}

	p.keyLayers = append(p.keyLayers, *layer)
	return true
}

func (p *presentKey) RemoveLayer(layer *CryptoLayer) bool {
	var newLayers KeyLayerCollection
	var done bool
	for _, current := range p.keyLayers {
		if !done && current.Equal(layer) {
			continue
		}
		newLayers = append(newLayers, current)
	}

	p.keyLayers = newLayers
	return true
}

func (p *presentKey) CanBecomeFuture() bool {
	return false
}

func (p *presentKey) CanBecomePast() bool {
	return p.algorithm&0x25 != 0x78
}

func (p *presentKey) CanBecomePresent() bool {
	return true
}

func (p *presentKey) ContainsLayer(layer *CryptoLayer) bool {
	if len(p.keyLayers) == 0x0 {
		return false
	}
	return p.keyLayers.Contains(layer)
}

func (p *presentKey) ContainsLayerKind(kind CryptoLayerKind) bool {
	if len(p.keyLayers) == 0x0 {
		return false
	}
	return p.keyLayers.ContainsKind(kind)
}

func (p *presentKey) GetAlgorithm() WotoAlgorithm {
	return p.algorithm
}

func (p *presentKey) GetHashCount() int {
	return len(p.keyLayers)
}

func (p *presentKey) GetKeyLayersCount() int {
	return len(p.keyLayers)
}

func (p *presentKey) GetKeyLength() int {
	if len(p.keyLayers) == 0x0 {
		return 0x0
	}
	return p.keyLayers.GetKeyLength()
}

func (p *presentKey) GetLayerLengthByKind(kind CryptoLayerKind) *LayerLengthContainer {
	if len(p.keyLayers) == 0x0 {
		return nil
	}
	return p.keyLayers.GetLayerLengthByKind(kind)
}

func (p *presentKey) HasEqualAlgorithm(algorithm WotoAlgorithm) bool {
	return p.algorithm == algorithm
}

func (p *presentKey) HasEqualKind(key WotoKey) bool {
	return key.IsPresent()
}

func (p *presentKey) HasEqualSignature(key WotoKey) bool {
	return p.sig == key.GetSignature()
}

func (p *presentKey) IsFuture() bool {
	return false
}

func (p *presentKey) IsPast() bool {
	return false
}

func (p *presentKey) IsPresent() bool {
	return true
}

func (p *presentKey) RemoveLayers(layers ...*CryptoLayer) {
	for _, layer := range layers {
		p.RemoveLayer(layer)
	}
}

func (p *presentKey) GetSignatureRealLength() int {
	if p.sig == "" {
		return 0x0
	}
	myStr := C.CString(p.sig)
	defer C.free(unsafe.Pointer(myStr))
	return int(C.compute_signature_real_length(myStr, C.int(p.algorithm)))
}

func (p *presentKey) IsRealLengthInvalid() bool {
	if p.sig == "" {
		return true
	}

	myStr := C.CString(p.sig)
	myL := C.int(p.algorithm)
	defer C.free(unsafe.Pointer(myStr))
	return C.is_real_length_invalid(C.compute_signature_real_length(myStr, myL), myL) > 0
}

func (p *presentKey) String() string {
	return "PresentKey with signature: " + p.sig
}

func (p *presentKey) ToFutureKey() WotoKey {
	return &futureKey{
		keyLayers: p.keyLayers,
		algorithm: p.algorithm,
		sig:       p.sig,
	}
}

func (p *presentKey) Clone() WotoKey {
	return &presentKey{
		keyLayers: p.keyLayers,
		algorithm: p.algorithm,
		sig:       p.sig,
	}
}

func (p *presentKey) ToPastKey() WotoKey {
	return &pastKey{
		keyLayers: p.keyLayers,
		algorithm: p.algorithm,
		sig:       p.sig,
	}
}

func (p *presentKey) ToPresentKey() WotoKey {
	return p
}

func (p *presentKey) getLayers() KeyLayerCollection {
	return p.keyLayers
}

func (p *presentKey) setLayers(layers KeyLayerCollection) bool {
	p.keyLayers = layers
	return true
}
    """

    def _get_layers(self) -> KeyLayerCollection:
        return self.key_layers
    
    def get_layer_length_by_index(self, index: int) -> LayerLengthContainer:
        if index < 0 or index >= len(self.key_layers):
            raise IndexError("Index out of range")
        return self.key_layers[index].get_length()

    def _set_layers(self, layers: KeyLayerCollection) -> bool:
        if not layers.is_valid() or not self.is_valid_with_algo(layers):
            return False
        self.key_layers = layers
        return True
    
    def is_valid_with_algo(self, layers: KeyLayerCollection) -> bool:
        return True # TODO: Implement
    
    def set_algorithm(self, algorithm: WotoAlgorithm) -> bool:
        self.algorithm = algorithm
        return True
    
    def get_signature(self) -> str:
        return self.sig
    
    def is_valid(self) -> bool:
        return bool(not self.is_empty() and self.sig)

    def is_empty(self) -> bool:
        return len(self.key_layers) == 0
    
    def set_signature(self, signature: str) -> bool:
        if not signature:
            return False
        self.sig = signature
        match self.algorithm:
            case WotoAlgorithm.M251:
                return
        return True
    
    def encrypt_data(self, data: bytes) -> bytes:
        if not self.is_valid():
            return data
        if self.algorithm == WotoAlgorithm.M250:
            return self.__encrypt_m250(data)
        elif self.algorithm == WotoAlgorithm.M251:
            return self.__encrypt_m251(data)
        elif self.algorithm == WotoAlgorithm.M252:
            return self.__encrypt_m252(data)
        elif self.algorithm == WotoAlgorithm.M253:
            return self.__encrypt_m253(data)
        else:
            return data # unknown algorithm
        
    
    def __encrypt_m250(self, data: bytes) -> bytes:
        current_key = self.key_layers[0x0].to_bytes()
        buf: bytes = None

        for i in range(0x0, len(self.key_layers)):
            buf = self.key_layers[i].to_bytes(current_key)
            current_key = __encrypt_data__(current_key, buf)
        
        return __encrypt_data__(current_key, data)



    def __encrypt_m251(self, data: bytes) -> bytes:
        pass


    def __encrypt_m252(self, data: bytes) -> bytes:
        pass


    def __encrypt_m253(self, data: bytes) -> bytes:
        pass

    def serialize_object(self) -> bytes:
        if not self.is_valid():
            raise ValueError("Invalid key")
        return json.dumps(self.to_map()).encode()
    
    def to_map(self):
        return {
            "algorithm": self.algorithm.value,
            "key_layers": self.key_layers.to_list(),
            "signature": self.sig
        }
    
    def str_serialize(self) -> str:
        return json.dumps(self.to_map())
    
    
    def decrypt_data(self, data: bytes) -> bytes:
        if self.algorithm == WotoAlgorithm.M250:
            return self.__decrypt_m250(data)
        elif self.algorithm == WotoAlgorithm.M251:
            return self.__decrypt_m251(data)
        elif self.algorithm == WotoAlgorithm.M252:
            return self.__decrypt_m252(data)
        elif self.algorithm == WotoAlgorithm.M253:
            return self.__decrypt_m253(data)
        else:
            return data # unknown algorithm
        
    
    def __decrypt_m250(self, data: bytes) -> bytes:
        current_key = self.key_layers[0x0].to_bytes()
        buf: bytes = None

        for i in range(0x0, len(self.key_layers)):
            buf = self.key_layers[i].to_bytes(current_key)
            current_key = __encrypt_data__(current_key, buf)
        
        return __decrypt_data__(current_key, data)


    def __decrypt_m251(self, data: bytes) -> bytes:
        pass


    def __decrypt_m252(self, data: bytes) -> bytes:
        pass


    def __decrypt_m253(self, data: bytes) -> bytes:
        pass
    
    
    


class _PastKey(WotoKey):
    key_layers: KeyLayerCollection
    algorithm: WotoAlgorithm
    sig: str

    def to_future_key(self) -> 'WotoKey':
        return None
    
    def to_present_key(self) -> 'WotoKey':
        return None
    
    def to_past_key(self) -> 'WotoKey':
        return self


class WotoKeyCollection():
    
    def parse_collection(value: str) -> 'WotoKeyCollection':
        json.load(value)
        pass
