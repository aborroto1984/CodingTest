import React, { useState } from 'react';
import axios from 'axios';

function ProductForm() {
  const [productName, setProductName] = useState('');
  const [productSku, setProductSku] = useState('');
  const [productTypeName, setProductTypeName] = useState('');
  const [confirmation, setConfirmation] = useState('');


  const handleAddProduct = async () => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/create_product/${productName}/${productSku}/${productTypeName}/`);

      console.log(response.status)

      setProductName('');
      setProductSku('');
      setProductTypeName('');


      if (response.status === 200) {
        console.log('Product created successfully.');
        setConfirmation('Product created successfully.');

      } else {
        console.error('Product creation failed.');
        setConfirmation('Product creation failed.');
  
      }
    } catch (error) {
      console.error('Error:', error);
      setConfirmation('Error: Product creation failed.');

    }
  };

  const handleClearForm = () => {
    setProductName('');
    setProductSku('');
    setProductTypeName('');
    setConfirmation('');
  };

  return (
    <div className="container">
      <h2>Add Product</h2>
      <form>
        <div>
          <label>
            Product Name:
            <input type="text" value={productName} onChange={(e) => setProductName(e.target.value)} />
          </label>
        </div>
        <div>
          <label>
            Product SKU:
            <input type="text" value={productSku} onChange={(e) => setProductSku(e.target.value)} />
          </label>
        </div>
        <div>
          <label>
            Product Type:
            <input type="text" value={productTypeName} onChange={(e) => setProductTypeName(e.target.value)} />
          </label>
        </div>
        <div>
          <button type="button" onClick={handleAddProduct}>Add Product</button>
          <button type="button" onClick={handleClearForm}>Clear Form</button>
        </div>
      </form>
      {confirmation && <div className="confirmation">{confirmation}</div>}
    </div>
  );
}

export default ProductForm;
